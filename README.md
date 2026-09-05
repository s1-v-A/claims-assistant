# Claims Evidence Review Assistant (NexusTiQ 24)

An automated, AI-powered insurance claims auditing system built with **FastAPI**, **Google Gemini**, and a custom web interface.

---

## Executive Summary

The **Claims Evidence Review Assistant** simplifies and accelerates the insurance claims evaluation process. By analyzing structured claim JSON payloads alongside unstructured medical evidence documents (PDFs, invoices, diagnostic reports), the assistant automatically:

1. **Cross-examines claim data** against attached documents.
2. **Detects discrepancies and contradictions** (e.g., date mismatches, unbilled services, procedure code conflicts).
3. **Evaluates policy rules** line-by-line to ensure full policy compliance.
4. **Outputs a structured audit report** complete with executive recommendations (`APPROVE`, `REJECT`, `REQUEST_INFO`, `ESCALATE`), clause citations, and detailed reasoning.

---

## ✨ Key Features

- **Multi-Modal Evidence Analysis:** Upload supporting medical documents (PDF format) directly alongside structured JSON claims.
- **Pre-Loaded Sample Docs:** Located in `/sample_docs` for quick, zero-setup testing of PDF evidence uploads during evaluation.
- **Rule-by-Rule Policy Verification:** Cross-references policy terms line-by-line, flagging each as `SUPPORTED`, `VIOLATED`, or `NOT_APPLICABLE`.
- **Discrepancy & Contradiction Engine:** Automatically surfaces conflicts between claimed amounts, dates, or services vs. actual medical records.
- **Preset Demo Cases:** Pre-loaded claim cases for instant, one-click demonstration during reviews.
- **Executive Dashboard:** Clean, visual UI displaying color-coded decision badges, audit tables, and breakdown logic.

## System Architecture

```text
+-------------------------+
|     Client Frontend     |
| (JSON + Optional PDF)   |
+------------+------------+
             |
             | HTTP POST Request
             v
+-------------------------+
|     FastAPI Backend     |
|  (/api/analyze-upload)  |
+------------+------------+
             |
             | Multi-modal Analysis
             v
+-------------------------+
|   Google Gemini Engine  |
| (Policy & Fraud Engine) |
+------------+------------+
             |
             | Structured Audit Payload
             v
+-------------------------+
|   Rendered Audit Report |
|   (Decision, Table,     |
|    Discrepancies)       |
+-------------------------+
```

1. **Input Submission:** Users select a pre-configured test case or paste a custom JSON claim package. Optionally, a supporting PDF FIR/Medical documents can be uploaded (Located in `/sample_docs`)
2. **Backend Processing:** FastAPI processes the incoming request, parses the multipart data, and extracts relevant medical text or document tokens.
3. **LLM Evaluation:** Data is fed into **Google Gemini 3.5 Flash Lite** with tailored system instructions to cross-reference data points and evaluate specific policy terms.
4. **Structured Audit Output:** The model returns structured evaluation metrics, which are rendered dynamically in an executive dashboard format.



## Getting Started

## Prerequisites

- **Python 3.9+**
- A **Google Gemini API Key** (for Gemini 3.5 Flash Lite)

### Installation

1. **Clone the repository:**
   git clone https://github.com/s1-v-A/claims-assistant.git

   cd claim-evidence-review-assistant

2. **Set up a virtual environment:**
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install dependencies:**
   pip install -r requirements.txt

4. **Environment Setup:**
   Create a .env file in the root directory and add your Gemini API key:
   GEMINI_API_KEY=api_key_here

---

## Running the Application

1. **Start the Application Server:**
   python app.py

2. **Access the Web Dashboard:**
   Open your browser and navigate to: http://localhost:8000

3. **Explore API Documentation:**
   Interactive Fastapi Swagger documentation is available at: http://localhost:8000/docs

---

## Project Structure

claims-assistant/               <-- Parent Folder
├── data/                       <-- place for backend JSON rules/data
│   ├── policy.json
│   └── sample_claims.json
├── sample_docs/                <-- Sample PDFs/files for users to test uploads
├── src/                        <-- Helper modules/logic
├── static/                     <-- Front-end UI files
│   └── index.html
├── .env.example                <-- PUBLIC: Template showing required env key names
├── .gitignore                  <-- Git rules file
├── app.py                      <-- FastAPI server entry point
├── README.md                   # Complete documentation
└── requirements.txt            # Python dependencies

---

## API Endpoints

## API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Serves the main web dashboard UI |
| `GET` | `/api/sample-cases` | Returns list of preset JSON claim cases |
| `POST` | `/api/analyze` | Audits a standalone JSON claim package |
| `POST` | `/api/analyze-upload` | Audits a JSON claim package with an attached PDF document |

---

## Tech Stack

- **Backend:** FastAPI, Uvicorn, Pydantic
- **AI/LLM:** Google Gemini 3.5 Flash Lite
- **Frontend:** HTML5, CSS3 (Custom responsive styling), JavaScript (Fetch API)

---

## License

This project is open-source and available under the [MIT License](LICENSE).