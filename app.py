import json
from pathlib import Path
from typing import Optional

from anyio import Path as AsyncPath
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src.engine import ClaimReviewReport, evaluate_claim, extract_text_from_pdf

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="NexusTiQ 24 - Claims Evidence Review Assistant",
    description="Automated AI Auditor for Motor Insurance Claims Evaluation",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


class AnalysisRequest(BaseModel):
    claim_package: dict


@app.get("/")
async def read_root():
    """Serves the main investigator dashboard HTML."""
    index_path = BASE_DIR / "static" / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=500, detail="static/index.html template not found.")
    return FileResponse(index_path, media_type="text/html")


@app.get("/api/sample-cases")
async def get_sample_cases():
    """Returns preset test claims from sample_claims.json asynchronously."""
    sample_path = AsyncPath(BASE_DIR / "data" / "sample_claims.json")
    if not await sample_path.exists():
        raise HTTPException(status_code=404, detail="sample_claims.json not found in data/ directory.")
    
    try:
        content = await sample_path.read_text(encoding="utf-8")
        return json.loads(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load sample cases: {str(e)}")


@app.post("/api/analyze", response_model=ClaimReviewReport)
async def analyze_claim(request: AnalysisRequest):
    """Processes a raw JSON claim package via standard JSON body."""
    try:
        return evaluate_claim(claim_package=request.claim_package)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audit execution failed: {str(e)}")


@app.post("/api/analyze-upload", response_model=ClaimReviewReport)
async def analyze_claim_upload(
    claim_json: str = Form(...),
    document: Optional[UploadFile] = File(None)
):
    """Processes a JSON claim package alongside an optional PDF evidence file upload."""
    try:
        claim_package = json.loads(claim_json)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON string in claim_json: {str(e)}")

    extracted_text = None
    if document:
        if not document.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are supported currently.")
        
        pdf_bytes = await document.read()
        extracted_text = extract_text_from_pdf(pdf_bytes)

    try:
        return evaluate_claim(claim_package=claim_package, extracted_doc_text=extracted_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audit execution failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)