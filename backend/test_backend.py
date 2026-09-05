"""
Comprehensive Verification Suite for IP-SAKTI Sahayak (LangChain Powered).
Validates vector retrieval, classifier state machine, grounding gates, rule checks, and REST API endpoints.
"""

import sys
import os
from fastapi.testclient import TestClient

# Add app directory to python path
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))
sys.path.append(os.path.dirname(__file__))

from seed_corpus import generate_seed_corpus
from ingest import ingest_corpus
from classifier import process_classification_step, get_initial_question
from retriever import retrieve_chunks
from citation_validator import validate_citations
from llm import generate_grounded_answer
from rule_checks import check_abs_compliance, check_tkdl_pointer
from eval_engine import run_evaluation_benchmark
from database import init_db
from main import app

def test_full_langchain_pipeline():
    print("1. Initializing database...")
    init_db()

    print("2. Generating seed corpus and building LangChain vector index...")
    generate_seed_corpus()
    ingest_res = ingest_corpus()
    print(f"   Ingested {ingest_res['total_chunks']} LangChain Document chunks.")
    assert ingest_res['total_chunks'] > 0

    print("3. Testing formulation state machine...")
    state1 = process_classification_step({})
    assert state1["status"] == "in_progress"
    
    state2 = process_classification_step({"q1_base": "classical"})
    assert state2["status"] == "completed"
    assert state2["category_key"] == "classical"

    state3 = process_classification_step({"q1_base": "food_wellness", "q2_food": "yes"})
    assert state3["status"] == "completed"
    assert state3["category_key"] == "ayurveda_aahar"

    print("4. Testing LangChain retriever & jurisdiction filter...")
    india_chunks, conf, score = retrieve_chunks("Can I patent traditional knowledge?", jurisdiction="india")
    assert len(india_chunks) > 0
    assert all(c["metadata"]["jurisdiction"] == "india" for c in india_chunks)
    assert "langchain_doc" in india_chunks[0]

    intl_chunks, conf_intl, score_intl = retrieve_chunks("What is Nagoya Protocol benefit sharing?", jurisdiction="international")
    assert len(intl_chunks) > 0
    assert all(c["metadata"]["jurisdiction"] == "international" for c in intl_chunks)

    print("5. Testing LangChain LLM grounded generation & hard-gate validator...")
    answer = generate_grounded_answer("Can I patent traditional knowledge?", india_chunks, "india")
    is_valid, citations, final_ans, err, r_type = validate_citations(answer, india_chunks, conf, query="Can I patent traditional knowledge?", top_score=score)
    assert is_valid == True
    assert len(citations) > 0

    print("6. Testing domain guardrails (greetings, out-of-domain rejection, ungrounded queries)...")
    # Greetings test
    _, _, greet_ans, _, greet_rtype = validate_citations("Hi!", [], "Low", query="hii", top_score=0.0)
    assert greet_rtype == "greeting"
    assert "IP-SAKTI Sahayak" in greet_ans

    # Out of domain query test
    _, _, ood_ans, _, ood_rtype = validate_citations("2+2=4", [], "Low", query="2+2", top_score=0.0)
    assert ood_rtype == "out_of_domain"
    assert "outside the domain" in ood_ans.lower()

    # Ungrounded in-domain query test
    bad_chunks, bad_conf, bad_score = retrieve_chunks("How to build a space rocket motor with Ayush herbs?", jurisdiction="india")
    is_valid_bad, citations_bad, final_ans_bad, err_bad, r_type_bad = validate_citations("Space rocket motor patent [Space Act - Section 1]", bad_chunks, bad_conf, query="How to build a space rocket motor with Ayush herbs?", top_score=bad_score)
    assert is_valid_bad == False
    assert r_type_bad == "ungrounded"
    assert "don't have" in final_ans_bad.lower() or "knowledge" in final_ans_bad.lower()

    print("7. Testing ABS compliance and TKDL pointers...")
    abs_res = check_abs_compliance("Need export biological resource NBA clearance", india_chunks)
    assert abs_res["triggered"] == True
    
    tkdl_res = check_tkdl_pointer("proprietary", "patent formulation")
    assert tkdl_res["triggered"] == True

    print("8. Running benchmark evaluation suite on LangChain backend...")
    eval_res = run_evaluation_benchmark("LangChain Unit Test Run")
    print(f"   LangChain Eval Precision@k: {eval_res['precision_at_k']}, Citation Validity: {eval_res['citation_validity_rate']}")

    print("9. Testing all FastAPI REST endpoints via TestClient...")
    client = TestClient(app)

    # Health check
    res_health = client.get("/api/health")
    assert res_health.status_code == 200
    assert res_health.json()["status"] == "online"

    # Start classifier
    res_start = client.get("/api/classifier/start")
    assert res_start.status_code == 200
    assert "question" in res_start.json()

    # Classify step
    res_classify = client.post("/api/classify", json={"session_id": "test_sess", "answers": {"q1_base": "phytopharma"}})
    assert res_classify.status_code == 200
    assert res_classify.json()["status"] == "completed"

    # Chat asking unclassified query (should return needs_classification)
    res_chat_need = client.post("/api/chat", json={
        "query": "Can I patent my formulation?",
        "jurisdiction": "india",
        "session_id": "test_sess_1",
        "classification_answers": {}
    })
    assert res_chat_need.status_code == 200
    assert res_chat_need.json()["needs_classification"] == True

    # Chat with completed classification
    res_chat_done = client.post("/api/chat", json={
        "query": "Can I patent traditional knowledge?",
        "jurisdiction": "india",
        "session_id": "test_sess_2",
        "override_classification": "Classical Ayurvedic Formulation"
    })
    assert res_chat_done.status_code == 200
    assert res_chat_done.json()["needs_classification"] == False
    assert "answer" in res_chat_done.json()
    assert len(res_chat_done.json()["citations"]) > 0

    # Escalate to expert
    res_esc = client.post("/api/escalate", json={
        "name": "Dr. Test Practitioner",
        "email": "test@ayush.org",
        "query": "Need help registering proprietary tablet with NBA",
        "product_category": "Proprietary Ayurvedic Medicine",
        "jurisdiction": "india",
        "notes": "Testing escalation pipeline"
    })
    assert res_esc.status_code == 200
    assert res_esc.json()["status"] == "success"

    # Metrics & Benchmark run
    res_metrics = client.get("/api/metrics")
    assert res_metrics.status_code == 200
    assert "eval_runs" in res_metrics.json()

    print("\n[SUCCESS] ALL BACKEND PIPELINES & REST API ENDPOINTS PASSED CLEANLY (100% OPERATIONAL)!")

if __name__ == "__main__":
    test_full_langchain_pipeline()
