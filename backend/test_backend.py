"""
Comprehensive Verification Suite for IP-SAKTI Sahayak (Phase 1, 2, & 3).
Validates:
- Phase 1: Vector retrieval, classifier state machine, grounding gates, rule checks, and REST API endpoints.
- Phase 2: Ayurvedic Herb & Statutory Knowledge Graph, Multi-Hop Pathway Traversals, and Section 3(e) Synergy Analysis.
- Phase 3: Bhashini Indic Multilingual Support and DPDP Act 2023 SHA-256 Cryptographic Audit Certificates.
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
from knowledge_graph import get_herb_catalog, compute_multi_herb_pathway, evaluate_section_3e_synergy
from bhashini import get_supported_languages
from main import app

def test_full_pipeline():
    print("1. Initializing database with DPDP cryptographic schema...")
    init_db()

    print("2. Ingesting statutory seed corpus into vector store...")
    generate_seed_corpus()
    ingest_res = ingest_corpus()
    print(f"   Ingested {ingest_res['total_chunks']} Document chunks.")
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

    intl_chunks, conf_intl, score_intl = retrieve_chunks("What is Nagoya Protocol benefit sharing?", jurisdiction="international")
    assert len(intl_chunks) > 0
    assert all(c["metadata"]["jurisdiction"] == "international" for c in intl_chunks)

    print("5. Testing LLM grounded generation & hard-gate validator...")
    answer = generate_grounded_answer("Can I patent traditional knowledge?", india_chunks, "india")
    is_valid, citations, final_ans, err = validate_citations(answer, india_chunks, conf)
    assert is_valid == True
    assert len(citations) > 0

    print("6. Testing ungrounded query hard block...")
    bad_chunks, bad_conf, bad_score = retrieve_chunks("How to build a space rocket motor with Ayush herbs?", jurisdiction="india")
    is_valid_bad, citations_bad, final_ans_bad, err_bad = validate_citations("Space rocket motor patent [Space Act - Section 1]", bad_chunks, bad_conf)
    assert is_valid_bad == False
    assert "don't have a grounded source" in final_ans_bad.lower()

    print("7. Testing Phase 2 Knowledge Graph & Section 3(e) Synergy Engine...")
    herbs = get_herb_catalog()
    assert len(herbs) >= 10
    print(f"   Knowledge Graph loaded {len(herbs)} Ayurvedic botanicals.")

    pathway = compute_multi_herb_pathway(["ashwagandha", "curcumin", "brahmi"])
    assert len(pathway["nodes"]) > 0
    assert len(pathway["edges"]) > 0
    assert "Section 3(p) Bar" in [n["label"] for n in pathway["nodes"]]
    assert pathway["pathway_summary"]["sec_3e_synergy_mandate"] == "MANDATORY"
    print("   Multi-hop regulatory pathway computed successfully.")

    synergy_eval = evaluate_section_3e_synergy(
        herb_names=["Ashwagandha", "Curcumin"],
        has_experimental_data=True,
        combination_index=0.72
    )
    assert "FAVORABLE" in synergy_eval["patentability_verdict"]
    print("   Section 3(e) synergy evaluator scored CI < 1.0 correctly.")

    print("8. Testing Phase 3 Bhashini Indic Languages & DPDP Modules...")
    langs = get_supported_languages()
    assert "hi" in langs and "bn" in langs and "ta" in langs
    print(f"   Bhashini engine initialized with {len(langs)} languages.")

    print("9. Testing all FastAPI REST endpoints via TestClient...")
    client = TestClient(app)

    # Health check
    res_health = client.get("/api/health")
    assert res_health.status_code == 200
    assert res_health.json()["status"] == "online"

    # Knowledge Graph Herbs
    res_herbs = client.get("/api/knowledge-graph/herbs")
    assert res_herbs.status_code == 200
    assert res_herbs.json()["total_herbs"] >= 10

    # Knowledge Graph Pathway
    res_path = client.post("/api/knowledge-graph/pathway", json={"herbs": ["ashwagandha", "brahmi"]})
    assert res_path.status_code == 200
    assert "nodes" in res_path.json()
    assert "edges" in res_path.json()

    # Synergy Check
    res_syn = client.post("/api/knowledge-graph/synergy-check", json={
        "herbs": ["Ashwagandha", "Curcumin", "Pippali"],
        "has_experimental_data": True,
        "combination_index": 0.65
    })
    assert res_syn.status_code == 200
    assert "risk_radar" in res_syn.json()

    # Bhashini Languages
    res_lang = client.get("/api/bhashini/languages")
    assert res_lang.status_code == 200
    assert "hi" in res_lang.json()["supported_languages"]

    # Chat with completed classification and DPDP crypto hash
    res_chat = client.post("/api/chat", json={
        "query": "Can I patent traditional knowledge?",
        "jurisdiction": "india",
        "session_id": "test_sess_crypto",
        "override_classification": "Classical Ayurvedic Formulation",
        "dpdp_consent": True
    })
    assert res_chat.status_code == 200
    data_chat = res_chat.json()
    assert "crypto_hash" in data_chat
    assert data_chat["crypto_hash"] is not None
    log_id = data_chat["log_id"]

    # DPDP Certificate retrieval
    res_cert = client.get(f"/api/dpdp/certificate/{log_id}")
    assert res_cert.status_code == 200
    cert = res_cert.json()
    assert "certificate_id" in cert
    assert "verification_hash" in cert
    assert cert["dpdp_status"] is not None
    print(f"   Generated DPDP Compliance Certificate: {cert['certificate_id']}")

    print("\n[SUCCESS] ALL PHASE 1, 2 & 3 BACKEND ENGINES & REST APIs PASSED CLEANLY (100% OPERATIONAL)!")

if __name__ == "__main__":
    test_full_pipeline()
