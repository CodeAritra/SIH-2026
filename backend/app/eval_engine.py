"""
Evaluation Engine for IP-SAKTI Sahayak (/metrics).
Computes Precision@k, Recall@k, MRR, Citation Validity Rate, and Abstention Rate over a benchmark query dataset.
"""

from typing import List, Dict, Any
from retriever import retrieve_chunks
from citation_validator import validate_citations
from llm import generate_grounded_answer
from database import log_eval_run

BENCHMARK_EVAL_SET = [
    {
        "id": "eval_1",
        "query": "Is traditional knowledge patentable under Indian law?",
        "jurisdiction": "india",
        "expected_source": "Patents Act, 1970 (India)",
        "expected_section": "Section 3(p)",
        "should_abstain": False
    },
    {
        "id": "eval_2",
        "query": "What are the disclosure rules for biological materials in patent applications?",
        "jurisdiction": "india",
        "expected_source": "Patents Act, 1970 (India)",
        "expected_section": "Section 6",
        "should_abstain": False
    },
    {
        "id": "eval_3",
        "query": "Do non-citizens need NBA clearance before applying for patents using Indian herbs?",
        "jurisdiction": "india",
        "expected_source": "Biological Diversity Act, 2002 (Amended 2023) (India)",
        "expected_section": "Section 3",
        "should_abstain": False
    },
    {
        "id": "eval_4",
        "query": "Can generic plant names like Tulsi or Triphala be registered as exclusive trademarks?",
        "jurisdiction": "india",
        "expected_source": "Trade Marks Act, 1999 (India)",
        "expected_section": "Section 9",
        "should_abstain": False
    },
    {
        "id": "eval_5",
        "query": "What is the definition of Ayurveda Aahar and can it claim disease cure?",
        "jurisdiction": "india",
        "expected_source": "FSSAI Ayurveda-Aahar Regulations, 2022/2024 (India)",
        "expected_section": "Regulation 4",
        "should_abstain": False
    },
    {
        "id": "eval_6",
        "query": "What are the rules regarding objectionable advertisements for Ayurvedic medicines?",
        "jurisdiction": "india",
        "expected_source": "Drugs and Magic Remedies (Objectionable Advertisements) Act, 1954 (India)",
        "expected_section": "Section 3",
        "should_abstain": False
    },
    {
        "id": "eval_7",
        "query": "What is mandatory disclosure under the 2024 WIPO Genetic Resources treaty?",
        "jurisdiction": "international",
        "expected_source": "WIPO Treaty on Intellectual Property, Genetic Resources and Associated Traditional Knowledge (2024) (International)",
        "expected_section": "Article 3",
        "should_abstain": False
    },
    {
        "id": "eval_8",
        "query": "How does the Nagoya Protocol enforce access and benefit sharing compliance?",
        "jurisdiction": "international",
        "expected_source": "Nagoya Protocol on Access and Benefit-Sharing (International)",
        "expected_section": "Article 5",
        "should_abstain": False
    },
    {
        "id": "eval_9",
        "query": "What are TRIPS rules regarding trade secret protection for herbal formulas?",
        "jurisdiction": "international",
        "expected_source": "TRIPS Agreement (WIPO/WTO) (International)",
        "expected_section": "Article 39",
        "should_abstain": False
    },
    {
        "id": "eval_10",
        "query": "What is the timeline for PCT international search reports?",
        "jurisdiction": "international",
        "expected_source": "Patent Cooperation Treaty (PCT) (International)",
        "expected_section": "Article 15",
        "should_abstain": False
    },
    {
        "id": "eval_11",
        "query": "What is the patent protection period for commercial space satellites under Ayush law?",
        "jurisdiction": "india",
        "expected_source": None,
        "expected_section": None,
        "should_abstain": True
    },
    {
        "id": "eval_12",
        "query": "How to register nuclear submarine propulsion in the Ayurvedic pharmacopoeia?",
        "jurisdiction": "india",
        "expected_source": None,
        "expected_section": None,
        "should_abstain": True
    }
]

def run_evaluation_benchmark(run_name: str = "Benchmark Run") -> Dict[str, Any]:
    total_queries = len(BENCHMARK_EVAL_SET)
    top_k = 5
    
    hits = 0
    total_reciprocal_rank = 0.0
    valid_citations_count = 0
    correct_abstentions_count = 0
    total_should_abstain = sum(1 for item in BENCHMARK_EVAL_SET if item["should_abstain"])
    
    details = []

    for item in BENCHMARK_EVAL_SET:
        query = item["query"]
        jurisdiction = item["jurisdiction"]
        exp_source = item["expected_source"]
        exp_section = item["expected_section"]
        should_abstain = item["should_abstain"]

        retrieved_chunks, confidence, top_score = retrieve_chunks(query, jurisdiction, top_k)
        
        # Check retrieval hit & rank
        hit_found = False
        rank = 0
        
        if not should_abstain and exp_source:
            for idx, c in enumerate(retrieved_chunks):
                title = c["metadata"]["source_title"]
                sec = c["metadata"]["source_section"]
                if exp_source.lower() in title.lower() and exp_section.lower() in sec.lower():
                    hit_found = True
                    rank = idx + 1
                    break
            
            if hit_found:
                hits += 1
                total_reciprocal_rank += 1.0 / rank

        # Test LLM answer & citation validator hard gate
        draft_answer = generate_grounded_answer(query, retrieved_chunks, jurisdiction)
        is_valid, citations, final_answer, fail_reason = validate_citations(draft_answer, retrieved_chunks, confidence)

        is_abstained = ("don't have a grounded source" in final_answer.lower() or not is_valid)

        if should_abstain and is_abstained:
            correct_abstentions_count += 1
        elif not should_abstain and is_valid:
            valid_citations_count += 1

        details.append({
            "id": item["id"],
            "query": query,
            "jurisdiction": jurisdiction,
            "expected_source": exp_source,
            "expected_section": exp_section,
            "hit_found": hit_found,
            "rank": rank if hit_found else 0,
            "top_score": top_score,
            "confidence": confidence,
            "top_retrieved_chunk": retrieved_chunks[0]["metadata"]["source_title"] if retrieved_chunks else None,
            "is_valid_citation": is_valid,
            "is_abstained": is_abstained,
            "correct_behavior": (is_abstained if should_abstain else hit_found and is_valid)
        })

    precision_at_k = round(hits / (total_queries - total_should_abstain), 4) if (total_queries - total_should_abstain) > 0 else 0.0
    recall_at_k = precision_at_k # In this single target benchmark, recall equals precision@k
    mrr = round(total_reciprocal_rank / (total_queries - total_should_abstain), 4) if (total_queries - total_should_abstain) > 0 else 0.0
    citation_validity_rate = round(valid_citations_count / (total_queries - total_should_abstain), 4) if (total_queries - total_should_abstain) > 0 else 0.0
    abstention_rate = round(correct_abstentions_count / total_should_abstain, 4) if total_should_abstain > 0 else 1.0

    run_id = log_eval_run(
        run_name=run_name,
        total_queries=total_queries,
        precision_at_k=precision_at_k,
        recall_at_k=recall_at_k,
        mrr=mrr,
        citation_validity_rate=citation_validity_rate,
        abstention_rate=abstention_rate,
        details=details
    )

    return {
        "run_id": run_id,
        "run_name": run_name,
        "total_queries": total_queries,
        "precision_at_k": precision_at_k,
        "recall_at_k": recall_at_k,
        "mrr": mrr,
        "citation_validity_rate": citation_validity_rate,
        "abstention_rate": abstention_rate,
        "details": details
    }
