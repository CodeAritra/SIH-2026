"""
FastAPI Server Entrypoint for IP-SAKTI Sahayak.
Provides REST APIs for Chat, Formulation Classifier, Escalation, and Evaluation Metrics.
"""

import sys
import os
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load .env from project root
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(dotenv_path=dotenv_path)

# Add app directory to python path
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

from database import init_db, log_query, log_escalation, get_latest_eval_runs, get_query_logs
from classifier import process_classification_step, is_classification_dependent, get_initial_question
from retriever import retrieve_chunks
from llm import generate_grounded_answer
from citation_validator import validate_citations
from rule_checks import check_abs_compliance, check_tkdl_pointer, get_registry_pointers
from eval_engine import run_evaluation_benchmark

app = FastAPI(
    title="IP-SAKTI Sahayak API",
    description="RAG-based Intellectual Property and Regulatory Guidance Assistant for Ayurvedic Innovators",
    version="1.0.0"
)

# Enable CORS for Vite frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_db()
    # Run initial benchmark run if database has no eval runs yet
    try:
        runs = get_latest_eval_runs(limit=1)
        if not runs:
            run_evaluation_benchmark("Initial Baseline Run")
    except Exception as e:
        print(f"Startup benchmark run error: {e}")

# Request/Response Schemas
class ChatRequest(BaseModel):
    query: str
    jurisdiction: str = "india"
    session_id: str = "default_session"
    classification_answers: Optional[Dict[str, str]] = None
    override_classification: Optional[str] = None

class ClassifyRequest(BaseModel):
    session_id: str = "default_session"
    answers: Dict[str, str]

class EscalateRequest(BaseModel):
    name: str
    email: str
    query: str
    product_category: Optional[str] = None
    jurisdiction: str = "india"
    notes: Optional[str] = None

class EvalRunRequest(BaseModel):
    run_name: Optional[str] = "Manual Benchmark Run"

STANDING_DISCLAIMER = "This is informational guidance, not legal advice."

@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "service": "IP-SAKTI Sahayak API",
        "database": "SQLite connected",
        "jurisdictions_supported": ["india", "international"]
    }

@app.post("/api/chat")
def chat_endpoint(req: ChatRequest):
    query = req.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    jurisdiction = req.jurisdiction.lower() if req.jurisdiction else "india"

    # Step 1: Check formulation classification status
    classification_answers = req.classification_answers or {}
    classifier_state = process_classification_step(classification_answers)
    
    product_category_name = req.override_classification
    category_key = "unclassified"

    if classifier_state["status"] == "completed":
        product_category_name = classifier_state["category_name"]
        category_key = classifier_state["category_key"]
    elif is_classification_dependent(query) and classifier_state["status"] == "in_progress" and not req.override_classification:
        # Require formulation classification before answering!
        return {
            "needs_classification": True,
            "classifier_question": classifier_state["next_question"],
            "explanation": (
                "Your query depends on the specific classification of your Ayurvedic product "
                "(e.g., Classical vs Proprietary vs Food/Nutraceutical). "
                "Please answer this quick question so I can apply the correct legal framework."
            ),
            "jurisdiction": jurisdiction,
            "disclaimer": STANDING_DISCLAIMER
        }

    if not product_category_name:
        product_category_name = "General Ayurvedic / Botanical Product"

    # Step 2: Retrieve grounded context chunks filtered by jurisdiction
    retrieved_chunks, confidence, top_score = retrieve_chunks(query, jurisdiction=jurisdiction, top_k=5)

    # Step 3: LLM reasoning with strict grounding prompt
    draft_answer = generate_grounded_answer(
        query=query,
        retrieved_chunks=retrieved_chunks,
        jurisdiction=jurisdiction,
        product_category=product_category_name
    )

    # Step 4: Hard-gate citation enforcement & domain boundary validator
    is_valid, citations, final_answer, fail_reason, response_type = validate_citations(
        llm_answer=draft_answer,
        retrieved_chunks=retrieved_chunks,
        min_confidence=confidence,
        query=query,
        top_score=top_score
    )

    # Step 5: ABS compliance & TKDL pointer rule checks (Only for in-domain legal queries!)
    if response_type in ["greeting", "out_of_domain"]:
        abs_alert = {"triggered": False, "title": None, "message": None}
        tkdl_pointer = {"triggered": False, "title": None, "message": None}
        registry_links = []
    else:
        abs_alert = check_abs_compliance(query, retrieved_chunks)
        tkdl_pointer = check_tkdl_pointer(category_key, query)
        registry_links = get_registry_pointers(retrieved_chunks)

    # Step 6: Log query to SQLite audit database
    log_id = log_query(
        session_id=req.session_id,
        user_query=query,
        jurisdiction=jurisdiction,
        classification=product_category_name,
        retrieved_chunks=retrieved_chunks,
        llm_raw_answer=draft_answer,
        citations=citations,
        confidence=confidence,
        is_blocked=not is_valid,
        abs_triggered=abs_alert["triggered"],
        tkdl_triggered=tkdl_pointer["triggered"]
    )

    # Append standing disclaimer to answer
    full_answer = f"{final_answer.strip()}\n\n---\n*{STANDING_DISCLAIMER}*"

    return {
        "log_id": log_id,
        "answer": full_answer,
        "citations": citations,
        "confidence": confidence,
        "top_score": top_score,
        "jurisdiction": jurisdiction,
        "product_category": product_category_name,
        "disclaimer": STANDING_DISCLAIMER,
        "is_blocked": not is_valid,
        "abs_alert": abs_alert if abs_alert["triggered"] else None,
        "tkdl_pointer": tkdl_pointer if tkdl_pointer["triggered"] else None,
        "registry_links": registry_links,
        "needs_classification": False
    }

@app.post("/api/classify")
def classify_endpoint(req: ClassifyRequest):
    state = process_classification_step(req.answers)
    return state

@app.get("/api/classifier/start")
def start_classifier():
    return get_initial_question()

@app.post("/api/escalate")
def escalate_endpoint(req: EscalateRequest):
    esc_id = log_escalation(
        name=req.name,
        email=req.email,
        user_query=req.query,
        product_category=req.product_category,
        jurisdiction=req.jurisdiction,
        notes=req.notes
    )
    return {
        "status": "success",
        "escalation_id": esc_id,
        "message": "Your escalation request has been submitted to Ayush & IP regulatory advisors."
    }

@app.get("/api/metrics")
def get_metrics():
    runs = get_latest_eval_runs(limit=10)
    query_logs = get_query_logs(limit=20)
    return {
        "eval_runs": runs,
        "recent_logs": query_logs
    }

@app.post("/api/metrics/run")
def trigger_eval_run(req: EvalRunRequest):
    run_result = run_evaluation_benchmark(req.run_name or "Manual Benchmark Run")
    return run_result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
