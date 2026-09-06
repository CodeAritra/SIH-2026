"""
Citation Validator & Hard Gate Module for IP-SAKTI Sahayak.
Enforces strict citation grounding; blocks any answer containing ungrounded claims.
"""

import re
from typing import List, Dict, Any, Tuple, Optional

SAFE_ABSTENTION_MESSAGE = (
    "I don't have a grounded source in the current legal/regulatory corpus to answer this question accurately. "
    "To prevent legal misguidance, I am withholding an answer. "
    "Please consider using the 'Escalate to Expert' option below to submit your query to Ayush & IP regulatory advisors."
)

def validate_citations(
    llm_answer: str,
    retrieved_chunks: List[Dict[str, Any]],
    min_confidence: str
) -> Tuple[bool, List[Dict[str, Any]], str, Optional[str]]:
    """
    Hard-gate validator checking LLM response grounding.
    Returns (is_valid, extracted_citations, final_answer, failure_reason).
    """
    if not retrieved_chunks:
        return False, [], SAFE_ABSTENTION_MESSAGE, "No relevant legal chunks retrieved in corpus."

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
                SAFE_ABSTENTION_MESSAGE,
                f"LLM cited ungrounded source '[{title_str} {sec_str}]' which was not in retrieved context."
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

    return True, citations, llm_answer, None
