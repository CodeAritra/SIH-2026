"""
Backend Verification Suite for IP-SAKTI Sahayak (LangChain Powered).
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

from seed_corpus import generate_seed_corpus
from ingest import ingest_corpus
from classifier import process_classification_step
from retriever import retrieve_chunks
from citation_validator import validate_citations
from llm import generate_grounded_answer
from rule_checks import check_abs_compliance, check_tkdl_pointer
from eval_engine import run_evaluation_benchmark
from database import init_db

def test_full_langchain_pipeline():
    print("1. Initializing database...")
    init_db()

    print("2. Generating seed corpus and building LangChain vector index...")
    generate_seed_corpus()
    ingest_res = ingest_corpus()
    print(f"Ingested {ingest_res['total_chunks']} LangChain Document chunks.")
    assert ingest_res['total_chunks'] > 0

    print("3. Testing formulation state machine...")
    state1 = process_classification_step({})
    assert state1["status"] == "in_progress"
    
    state2 = process_classification_step({"q1_base": "classical"})
    assert state2["status"] == "completed"
    assert state2["category_key"] == "classical"

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
    is_valid, citations, final_ans, err = validate_citations(answer, india_chunks, conf)
    assert is_valid == True
    assert len(citations) > 0

    print("6. Testing ungrounded query hard block...")
    bad_chunks, bad_conf, bad_score = retrieve_chunks("How to build a space rocket motor with Ayush herbs?", jurisdiction="india")
    is_valid_bad, citations_bad, final_ans_bad, err_bad = validate_citations("Space rocket motor patent [Space Act - Section 1]", bad_chunks, bad_conf)
    assert is_valid_bad == False
    assert "don't have a grounded source" in final_ans_bad.lower()

    print("7. Testing ABS compliance and TKDL pointers...")
    abs_res = check_abs_compliance("Need export biological resource NBA clearance", india_chunks)
    assert abs_res["triggered"] == True
    
    tkdl_res = check_tkdl_pointer("proprietary", "patent formulation")
    assert tkdl_res["triggered"] == True

    print("8. Running benchmark evaluation suite on LangChain backend...")
    eval_res = run_evaluation_benchmark("LangChain Unit Test Run")
    print(f"LangChain Eval Precision@k: {eval_res['precision_at_k']}, Citation Validity: {eval_res['citation_validity_rate']}")

    print("\nSUCCESS: All LangChain backend tests passed clean!")

if __name__ == "__main__":
    test_full_langchain_pipeline()
