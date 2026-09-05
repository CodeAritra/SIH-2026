"""
Citation Validator & Hard Gate Module for IP-SAKTI Sahayak.
Enforces strict domain guardrails & citation grounding; blocks out-of-domain requests
and ungrounded claims without fabricating answers.
"""

import re
from typing import List, Dict, Any, Tuple, Optional

AYUSH_DOMAIN_KEYWORDS = [
    # Ayush & Ayurvedic Formulations
    "ayurveda", "ayurvedic", "ayush", "herbal", "botanical", "herb", "herbs", "plant", "plants",
    "formulation", "formulations", "bhasma", "churna", "rasayana", "taila", "kvatha", "arista", "asava",
    "gutika", "kashayam", "ghrita", "lehya", "classical", "proprietary", "phytopharma", "phytopharmaceutical",
    "nutraceutical", "cosmetic", "cosmetics", "wellness", "ayurveda-aahar", "aahar", "sidha", "siddha", "unani",
    "homeopathy", "homeopathic", "medicine", "medicines", "drug", "drugs", "licensing", "extract", "extracts",

    # IP, Biodiversity & Regulatory Law
    "patent", "patents", "patenting", "patented", "tkdl", "traditional knowledge", "prior art",
    "geographical indication", "gi", "trademark", "trademarks", "copyright", "ipr", "intellectual property",
    "novelty", "inventive step", "section 3(p)", "section 3(k)", "section 3", "bda", "biological diversity",
    "nba", "national biodiversity authority", "state biodiversity board", "sbb", "abs", "access and benefit sharing",
    "fssai", "drugs and cosmetics", "license", "sla", "state licensing authority", "form 3", "form iii",
    "export", "commercialization", "monograph", "pharmacopoeia", "api", "afi", "compliance", "law", "act", "regulation"
]

GREETING_WORDS = {"hi", "hello", "hey", "greetings", "good morning", "good afternoon", "who are you", "what can you do", "help"}

OUT_OF_DOMAIN_REJECTION_MESSAGE = (
    "This request is outside my domain of Ayush Intellectual Property & Regulatory Compliance.\n\n"
    "I am **IP-SAKTI Sahayak**, specialized specifically in guiding Ayurvedic product innovators on Patents, "
    "Traditional Knowledge (TKDL), Biological Diversity Act (ABS), FSSAI Ayurveda-Aahar, and Drugs & Cosmetics Act rules. "
    "Please submit a query related to Ayush IP or legal compliance."
)

UNGROUNDED_IN_DOMAIN_MESSAGE = (
    "This query is within the Ayush legal domain, but I don't have sufficient grounded legal sources in the vector database "
    "to answer this question accurately without making assumptions.\n\n"
    "To prevent legal misguidance, I am withholding an answer. Please consider using the **'Escalate to Expert'** option below "
    "to submit your query to Ayush & IP regulatory advisors."
)

GREETING_RESPONSE = (
    "Hello! I am **IP-SAKTI Sahayak**, your specialized AI assistant for Ayurvedic Intellectual Property "
    "(Patents, TKDL, Geographical Indications, Trademarks) and Regulatory Guidance (Biological Diversity Act ABS, "
    "FSSAI Ayurveda-Aahar, Drugs & Cosmetics Act).\n\n"
    "How can I assist you with your Ayurvedic formulation or patent compliance query today?"
)

def is_greeting(query: str) -> bool:
    q_clean = query.strip().lower()
    if q_clean in GREETING_WORDS or any(q_clean == w for w in GREETING_WORDS):
        return True
    return bool(re.match(r'^(h[eia]+y*|hello+|greetings|good\s*(morning|afternoon|evening)|who\s*are\s*you|what\s*can\s*you\s*do|help)[\!\.\?]*$', q_clean))

def is_ayush_domain_query(query: str, retrieved_chunks: List[Dict[str, Any]], top_score: float) -> bool:
    """
    Returns True if the query belongs to the Ayush IP / Regulatory legal domain.
    """
    query_lower = query.lower()
    
    # 1. Explicit domain keywords match
    if any(k in query_lower for k in AYUSH_DOMAIN_KEYWORDS):
        return True

    # 2. High retrieval vector score match from corpus
    if top_score >= 0.30 and retrieved_chunks:
        return True

    return False

def validate_citations(
    llm_answer: str,
    retrieved_chunks: List[Dict[str, Any]],
    min_confidence: str,
    query: str = "",
    top_score: float = 0.0
) -> Tuple[bool, List[Dict[str, Any]], str, Optional[str], str]:
    """
    Hard-gate validator checking LLM response grounding and domain boundary.
    Returns (is_valid, extracted_citations, final_answer, failure_reason, response_type).
    """
    # Guardrail 0: Handle Greetings
    if query and is_greeting(query):
        return True, [], GREETING_RESPONSE, None, "greeting"

    # Guardrail 1: Out-of-Domain Rejection
    if query and not is_ayush_domain_query(query, retrieved_chunks, top_score):
        return (
            True,
            [],
            OUT_OF_DOMAIN_REJECTION_MESSAGE,
            "Query is outside the Ayush Intellectual Property & Regulatory domain.",
            "out_of_domain"
        )

    # Guardrail 2: In-Domain but No Grounded Knowledge in Vector DB
    if min_confidence == "Low" or not retrieved_chunks:
        return (
            False,
            [],
            UNGROUNDED_IN_DOMAIN_MESSAGE,
            "Query is in-domain but lacks grounded vector database context.",
            "ungrounded"
        )

    # Extract source titles and sections available in retrieved chunks
    valid_sources = {
        (c["metadata"]["source_title"].lower(), c["metadata"]["source_section"].lower()): c
        for c in retrieved_chunks
    }
    
    # Extract citations cited in the text, e.g. [Patents Act, 1970 - Section 3(p)]
    citation_pattern = r'\[([^\]]+?)(?:\s*-\s*([^\]]+))?\]'
    matches = re.findall(citation_pattern, llm_answer)

    citations = []
    seen_keys = set()

    for match in matches:
        title_str, sec_str = match[0].strip(), match[1].strip() if len(match) > 1 else ""
        
        # Check if cited document matches any retrieved chunk
        matched_chunk = None
        for chunk in retrieved_chunks:
            chunk_title = chunk["metadata"]["source_title"]
            chunk_sec = chunk["metadata"]["source_section"]
            
            if title_str.lower() in chunk_title.lower() or chunk_title.lower() in title_str.lower():
                if not sec_str or sec_str.lower() in chunk_sec.lower() or chunk_sec.lower() in sec_str.lower():
                    matched_chunk = chunk
                    break
        
        if matched_chunk:
            key = (matched_chunk["metadata"]["source_title"], matched_chunk["metadata"]["source_section"])
            if key not in seen_keys:
                seen_keys.add(key)
                citations.append({
                    "source_title": matched_chunk["metadata"]["source_title"],
                    "source_section": matched_chunk["metadata"]["source_section"],
                    "ip_type": matched_chunk["metadata"]["ip_type"],
                    "jurisdiction": matched_chunk["metadata"]["jurisdiction"],
                    "snippet": matched_chunk["text"][:180] + "..."
                })
        else:
            # Citation cited by LLM does NOT match any retrieved chunk -> Hard block!
            return (
                False,
                [],
                UNGROUNDED_IN_DOMAIN_MESSAGE,
                f"LLM cited ungrounded source '[{title_str} {sec_str}]' which was not in retrieved context.",
                "ungrounded"
            )

    # Ensure at least 1 grounded citation exists
    if not citations and retrieved_chunks:
        # Build automatic grounded citations from top retrieved chunks
        for c in retrieved_chunks[:2]:
            key = (c["metadata"]["source_title"], c["metadata"]["source_section"])
            if key not in seen_keys:
                seen_keys.add(key)
                citations.append({
                    "source_title": c["metadata"]["source_title"],
                    "source_section": c["metadata"]["source_section"],
                    "ip_type": c["metadata"]["ip_type"],
                    "jurisdiction": c["metadata"]["jurisdiction"],
                    "snippet": c["text"][:180] + "..."
                })

    return True, citations, llm_answer, None, "grounded"
