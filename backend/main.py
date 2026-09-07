"""
FastAPI Server Entrypoint for IP-SAKTI Sahayak.
Provides REST APIs for:
- Grounded RAG Chat & Formulation Classifier (Phase 1)
- Ayurvedic Herb & Statutory Knowledge Graph & Synergy Analyzer (Phase 2)
- Bhashini Indic Multilingual Translation & DPDP Act 2023 Cryptographic Audits (Phase 3)
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

from database import (
    init_db, log_query, log_escalation, get_latest_eval_runs,
    get_query_logs, get_query_log_by_id
)
from classifier import process_classification_step, is_classification_dependent, get_initial_question
from retriever import retrieve_chunks
from llm import generate_grounded_answer
from citation_validator import validate_citations
from rule_checks import check_abs_compliance, check_tkdl_pointer, get_registry_pointers
from eval_engine import run_evaluation_benchmark
from knowledge_graph import (
    get_herb_catalog, lookup_herb, compute_multi_herb_pathway, evaluate_section_3e_synergy
)
from bhashini import (
    get_supported_languages, get_ui_translations, translate_indic_text
)
from dpdp import (
    generate_tamper_evident_hash, generate_compliance_certificate
)

app = FastAPI(
    title="IP-SAKTI Sahayak API",
    description="RAG & Knowledge-Graph Grounded Intellectual Property and Regulatory Guidance for Ayurvedic Innovators",
    version="2.0.0"
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
    target_language: Optional[str] = "en"
    dpdp_consent: Optional[bool] = True

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

class PathwayRequest(BaseModel):
    herbs: List[str]
    target_ip: Optional[str] = "patent"
    jurisdiction: Optional[str] = "india"

class SynergyCheckRequest(BaseModel):
    herbs: List[str]
    extraction_method: Optional[str] = "Hydroalcoholic Standardized Extract"
    therapeutic_claim: Optional[str] = "Synergistic Anti-inflammatory and Neuroprotective"
    has_experimental_data: Optional[bool] = False
    combination_index: Optional[float] = None

class TranslateRequest(BaseModel):
    text: str
    target_language: str

STANDING_DISCLAIMER = "This is informational guidance, not legal advice."

@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "service": "IP-SAKTI Sahayak API v2.0 (Phase 1, 2 & 3 Enabled)",
        "database": "SQLite connected (DPDP SHA-256 enabled)",
        "jurisdictions_supported": ["india", "international"],
        "languages_supported": list(get_supported_languages().keys()),
        "knowledge_graph_herbs": len(get_herb_catalog())
    }

# ==========================================
# Phase 1: Core Grounded RAG Chat
# ==========================================
@app.post("/api/chat")
def chat_endpoint(req: ChatRequest):
    query = req.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    jurisdiction = req.jurisdiction.lower() if req.jurisdiction else "india"
    target_lang = req.target_language.lower() if req.target_language else "en"

    # Step 1: Check formulation classification status
    classification_answers = req.classification_answers or {}
    classifier_state = process_classification_step(classification_answers)
    
    product_category_name = req.override_classification
    category_key = "unclassified"

    if classifier_state["status"] == "completed":
        product_category_name = classifier_state["category_name"]
        category_key = classifier_state["category_key"]
    elif is_classification_dependent(query) and classifier_state["status"] == "in_progress" and not req.override_classification:
        # Translate question if needed
        q_text = classifier_state["next_question"]["question"]
        if target_lang != "en":
            q_text = translate_indic_text(q_text, target_lang)
            classifier_state["next_question"]["question"] = q_text

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

    # Step 4: Hard-gate citation enforcement validator
    is_valid, citations, final_answer, fail_reason, response_type = validate_citations(
        llm_answer=draft_answer,
        retrieved_chunks=retrieved_chunks,
        min_confidence=confidence,
        query=query,
        top_score=top_score
    )

    # Step 5: ABS compliance & TKDL pointer rule checks
    if response_type in ["greeting", "out_of_domain"]:
        abs_alert = {"triggered": False, "title": None, "message": None}
        tkdl_pointer = {"triggered": False, "title": None, "message": None}
        registry_links = []
    else:
        abs_alert = check_abs_compliance(query, retrieved_chunks)
        tkdl_pointer = check_tkdl_pointer(category_key, query)
        registry_links = get_registry_pointers(retrieved_chunks)

    # Step 6: Phase 3 DPDP SHA-256 Tamper-evident Hash
    crypto_hash = generate_tamper_evident_hash(
        session_id=req.session_id,
        user_query=query,
        jurisdiction=jurisdiction,
        classification=product_category_name,
        citations=citations,
        is_blocked=not is_valid
    )

    # Step 7: Log query to SQLite audit database
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
        tkdl_triggered=tkdl_pointer["triggered"],
        crypto_hash=crypto_hash,
        dpdp_consent=req.dpdp_consent if req.dpdp_consent is not None else True
    )

    # Step 8: Phase 3 Bhashini Multilingual Localization (if non-English)
    localized_answer = final_answer.strip()
    if target_lang != "en":
        localized_answer = translate_indic_text(localized_answer, target_lang)

    full_answer = f"{localized_answer}\n\n---\n*{STANDING_DISCLAIMER}*"

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
        "response_type": response_type,
        "crypto_hash": crypto_hash,
        "target_language": target_lang,
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

# ==========================================
# Phase 2: Ayurvedic Knowledge Graph & Synergy
# ==========================================
@app.get("/api/knowledge-graph/herbs")
def list_herbs():
    return {
        "total_herbs": len(get_herb_catalog()),
        "herbs": get_herb_catalog()
    }

@app.post("/api/knowledge-graph/pathway")
def get_pathway(req: PathwayRequest):
    if not req.herbs:
        raise HTTPException(status_code=400, detail="Please select at least one botanical herb.")
    pathway = compute_multi_herb_pathway(
        herb_ids=req.herbs,
        target_ip=req.target_ip or "patent",
        jurisdiction=req.jurisdiction or "india"
    )
    return pathway

@app.post("/api/knowledge-graph/synergy-check")
def synergy_check(req: SynergyCheckRequest):
    if not req.herbs:
        raise HTTPException(status_code=400, detail="Herbs list cannot be empty.")
    result = evaluate_section_3e_synergy(
        herb_names=req.herbs,
        extraction_method=req.extraction_method or "Hydroalcoholic Standardized Extract",
        therapeutic_claim=req.therapeutic_claim or "Anti-inflammatory and Neuroprotective",
        has_experimental_data=bool(req.has_experimental_data),
        combination_index=req.combination_index
    )
    return result

# ==========================================
# Phase 3: Bhashini & DPDP Cryptographic Audit
# ==========================================
@app.get("/api/bhashini/languages")
def get_languages():
    return {
        "supported_languages": get_supported_languages()
    }

@app.post("/api/bhashini/translate")
def translate_text(req: TranslateRequest):
    translated = translate_indic_text(req.text, req.target_language)
    return {
        "original_text": req.text,
        "translated_text": translated,
        "target_language": req.target_language
    }

@app.get("/api/dpdp/certificate/{log_id}")
def get_certificate(log_id: int):
    log_record = get_query_log_by_id(log_id)
    if not log_record:
        raise HTTPException(status_code=404, detail="Audit log record not found.")
    certificate = generate_compliance_certificate(log_record)
    return certificate

# ==========================================
# Escalation & Benchmark Metrics
# ==========================================
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