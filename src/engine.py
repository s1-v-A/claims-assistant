import json
import io
import os
from typing import List, Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
import pypdf

load_dotenv()

client = genai.Client()

class Discrepancy(BaseModel):
    issue: str = Field(description="Description of the factual mismatch")
    source_a: str = Field(description="First conflicting piece of evidence")
    source_b: str = Field(description="Second conflicting piece of evidence")

class PolicyRuleAudit(BaseModel):
    clause_id: str = Field(description="Policy clause ID, e.g., SEC_1_1")
    status: str = Field(description="SUPPORTED, VIOLATED, or NOT_APPLICABLE")
    reasoning: str = Field(description="Why this clause passed or failed")
    citation: str = Field(description="Direct text quote from submitted evidence")

class ClaimReviewReport(BaseModel):
    recommendation: str = Field(description="APPROVE, REJECT, REQUEST_INFO, or ESCALATE")
    summary: str = Field(description="Executive overview of the audit finding")
    discrepancies: List[Discrepancy] = Field(default=[], description="List of detected evidence contradictions")
    policy_audit: List[PolicyRuleAudit] = Field(default=[], description="Clause-by-clause policy alignment report")

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extracts clean text content from PDF binary data."""
    try:
        reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
        text = "".join(page.extract_text() or "" for page in reader.pages)
        return text.strip()
    except Exception as e:
        return f"Error parsing PDF document: {str(e)}"

def evaluate_claim(claim_package: dict, extracted_doc_text: Optional[str] = None) -> ClaimReviewReport:
    """Audits a claim package against grounding policy rules using Gemini 3.5 Flash Lite."""
    try:
        with open("data/policy.json", "r") as f:
            policy_data = json.load(f)
    except Exception as e:
        raise RuntimeError(f"Failed to load grounding policy rules: {str(e)}")

    doc_context = ""
    if extracted_doc_text:
        doc_context = f"\n\n--- ATTACHED DOCUMENT EVIDENCE ---\n{extracted_doc_text}\n-----------------------------------\n"

    prompt = f"""
You are an expert insurance claims auditor. Evaluate the submitted claim package against our official grounding policy rules.

--- GROUNDING POLICY RULES ---
{json.dumps(policy_data, indent=2)}

--- SUBMITTED CLAIM PACKAGE ---
{json.dumps(claim_package, indent=2)}
{doc_context}

INSTRUCTIONS:
1. Cross-examine all dates, locations, figures, and statements across all evidence.
2. Identify any contradictions or factual discrepancies.
3. Audit each relevant policy clause and determine if it is SUPPORTED, VIOLATED, or NOT_APPLICABLE.
4. Provide a clear recommendation: APPROVE, REJECT, REQUEST_INFO, or ESCALATE.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.1,
            response_mime_type="application/json",
            response_schema=ClaimReviewReport,
        ),
    )

    return ClaimReviewReport.model_validate_json(response.text)