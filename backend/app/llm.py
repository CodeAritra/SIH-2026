"""
Groq LLM Interface for IP-SAKTI Sahayak (LangChain Expression Language - LCEL).
Uses ChatGroq (llama-3.3-70b-versatile), ChatPromptTemplate, and StrOutputParser
with strict cite-or-abstain grounding system prompt.
Includes offline grounded fallback generator when GROQ_API_KEY is not provided.
"""

import os
import json
import logging
from typing import List, Dict, Any

from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser

logger = logging.getLogger(__name__)

SYSTEM_GROUNDING_PROMPT = """
You are IP-SAKTI Sahayak, an expert Intellectual Property and Regulatory Assistant for Ayurvedic product innovators.
Your primary directive is STRICT GROUNDED REASONING.

CRITICAL RULES YOU MUST FOLLOW:
1. Every factual claim in your answer MUST be explicitly grounded in the provided Legal/Regulatory Context chunks.
2. Every claim MUST be followed by a bracketed citation matching the source title and section exactly, e.g. [Patents Act, 1970 - Section 3(p)].
3. DO NOT extrapolate, guess, or bring in external knowledge not present in the provided context chunks.
4. Never mix Indian law and International law answers. Restrict your analysis strictly to the requested jurisdiction.
5. If the provided context chunks do not contain enough grounded information to answer the question, state: "I don't have a grounded source for this in the provided legal context."
6. Always maintain a professional, authoritative tone suitable for Ayush innovators and legal practitioners.
"""

def generate_grounded_answer(
    query: str,
    retrieved_chunks: List[Dict[str, Any]],
    jurisdiction: str,
    product_category: str = "Unspecified Formulation"
) -> str:
    """
    Calls LangChain ChatGroq LCEL chain or generates offline grounded fallback response.
    """
    groq_key = os.getenv("GROQ_API_KEY")

    # Format context chunks into readable text for LangChain prompt
    context_text = "\n\n".join([
        f"--- CONTEXT CHUNK {i+1} ---"
        f"\nSource Title: {c['metadata']['source_title']}"
        f"\nSource Section: {c['metadata']['source_section']}"
        f"\nJurisdiction: {c['metadata']['jurisdiction']}"
        f"\nIP Type: {c['metadata']['ip_type']}"
        f"\nText:\n{c['text']}"
        for i, c in enumerate(retrieved_chunks)
    ])

    if groq_key:
        try:
            from langchain_groq import ChatGroq
            candidate_models = [
                os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
                "llama-3.1-8b-instant",
                "llama3-70b-8192",
                "llama3-8b-8192",
                "mixtral-8x7b-32768"
            ]
        except ImportError as ie:
            logger.warning(f"langchain_groq not available: {ie}. Using offline generator.")
            candidate_models = []
        # Deduplicate while preserving order
        candidate_models = list(dict.fromkeys(candidate_models))

        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(SYSTEM_GROUNDING_PROMPT),
            HumanMessagePromptTemplate.from_template("""
USER JURISDICTION: {jurisdiction}
PRODUCT CATEGORY: {product_category}

USER QUERY:
"{query}"

RETRIEVED LEGAL CONTEXT CHUNKS:
{context_text}

INSTRUCTIONS:
Provide a clear, direct, grounded answer to the user query. Cite the specific source section in brackets after every legal point.
""")
        ])

        for model_name in candidate_models:
            try:
                llm = ChatGroq(
                    groq_api_key=groq_key,
                    model_name=model_name,
                    temperature=0.1,
                    max_tokens=800
                )

                # Build LangChain Expression Language (LCEL) chain
                chain = prompt | llm | StrOutputParser()

                result = chain.invoke({
                    "jurisdiction": jurisdiction.upper(),
                    "product_category": product_category,
                    "query": query,
                    "context_text": context_text
                })

                return result.strip()
            except Exception as e:
                logger.warning(f"ChatGroq with model '{model_name}' failed ({str(e)}).")
                continue

    # Offline grounded fallback generator
    if not retrieved_chunks:
        return "I don't have a grounded source for this in the provided legal context."

    lines = []
    lines.append(f"Based on **{jurisdiction.upper()}** legal framework for **{product_category}**:")
    
    for c in retrieved_chunks[:3]:
        title = c["metadata"]["source_title"]
        sec = c["metadata"]["source_section"]
        lines.append(f"\n• Under **[{title} - {sec}]**:")
        lines.append(f"  {c['text'].strip()}")

    lines.append("\n*Note: Ensure full compliance with State Licensing Authorities and National Biodiversity Authority protocols prior to commercial dispatch.*")
    return "\n".join(lines)
