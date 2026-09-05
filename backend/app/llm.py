"""
Gemini LLM Interface for IP-SAKTI Sahayak (LangChain Expression Language - LCEL).
Uses ChatGoogleGenerativeAI (gemini-1.5-flash / gemini-2.0-flash / gemini-1.5-pro),
ChatPromptTemplate, and StrOutputParser with strict cite-or-abstain grounding system prompt.
Includes offline grounded fallback generator when GEMINI_API_KEY is not provided or fails.
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
    Calls LangChain ChatGoogleGenerativeAI (Gemini) LCEL chain or generates offline grounded fallback response.
    """
    gemini_key = os.getenv("GEMINI_API_KEY")
    logger.info(f"[LLM] Using Gemini with key: {'YES' if gemini_key else 'NO'}")

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

    # Exclusive LLM Route: Google Gemini via LangChain & Native SDKs
    if gemini_key:
        models = ["gemini-3.5-flash-lite"]
        # Route A: LangChain ChatGoogleGenerativeAI
        logger.info("[LLM ROUTE A] Attempting LangChain ChatGoogleGenerativeAI pipeline...")
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            for gem_model in models:
                try:
                    logger.info(f"[LLM ROUTE A] Trying model '{gem_model}' via LangChain...")
                    llm = ChatGoogleGenerativeAI(
                        model=gem_model,
                        google_api_key=gemini_key,
                        temperature=0.1,
                        max_output_tokens=800
                    )
                    chain = prompt | llm | StrOutputParser()
                    result = chain.invoke({
                        "jurisdiction": jurisdiction.upper(),
                        "product_category": product_category,
                        "query": query,
                        "context_text": context_text
                    })
                    if result and result.strip():
                        logger.info(f"✅ [LLM SUCCESS] Answer successfully generated via Route A: LangChain ChatGoogleGenerativeAI ({gem_model})")
                        return result.strip()
                except Exception as gem_err:
                    logger.warning(f"❌ [LLM ROUTE A FAILED] Model '{gem_model}' error: {gem_err}")
        except Exception as e:
            logger.warning(f"❌ [LLM ROUTE A IMPORT FAILED] langchain_google_genai error: {e}")

        # Route B: Direct Google GenAI API Fallback (google.genai)
        logger.info("[LLM ROUTE B] Attempting direct google.genai SDK pipeline...")
        try:
            full_prompt = (
                f"{SYSTEM_GROUNDING_PROMPT}\n\n"
                f"USER JURISDICTION: {jurisdiction.upper()}\n"
                f"PRODUCT CATEGORY: {product_category}\n\n"
                f"USER QUERY:\n\"{query}\"\n\n"
                f"RETRIEVED LEGAL CONTEXT CHUNKS:\n{context_text}\n\n"
                f"INSTRUCTIONS:\n"
                f"Provide a clear, direct, grounded answer to the user query. Cite the specific source section in brackets after every legal point."
            )
            try:
                from google import genai
                from google.genai import types
                client = genai.Client(api_key=gemini_key)
                config = types.GenerateContentConfig(
                    temperature=0.1,
                    max_output_tokens=800
                )
                for g_model_name in models:
                    try:
                        logger.info(f"[LLM ROUTE B] Trying model '{g_model_name}' via google.genai SDK...")
                        response = client.models.generate_content(
                            model=g_model_name,
                            contents=full_prompt,
                            config=config
                        )
                        if response and response.text:
                            logger.info(f"✅ [LLM SUCCESS] Answer successfully generated via Route B: google.genai SDK ({g_model_name})")
                            return response.text.strip()
                    except Exception as g_err:
                        logger.warning(f"❌ [LLM ROUTE B FAILED] Model '{g_model_name}' error: {g_err}")
            except Exception as g_imp_err:
                logger.warning(f"❌ [LLM ROUTE B IMPORT FAILED] google.genai import error: {g_imp_err}")

            # Route C: Direct Google GenerativeAI API Fallback (google.generativeai)
            logger.info("[LLM ROUTE C] Attempting legacy google.generativeai SDK pipeline...")
            try:
                import google.generativeai as genai_legacy
                genai_legacy.configure(api_key=gemini_key)
                for g_model_name in models:
                    try:
                        logger.info(f"[LLM ROUTE C] Trying model '{g_model_name}' via google.generativeai SDK...")
                        g_model = genai_legacy.GenerativeModel(g_model_name)
                        res = g_model.generate_content(full_prompt)
                        if res and res.text:
                            logger.info(f"✅ [LLM SUCCESS] Answer successfully generated via Route C: google.generativeai SDK ({g_model_name})")
                            return res.text.strip()
                    except Exception as g_leg_err:
                        logger.warning(f"❌ [LLM ROUTE C FAILED] Model '{g_model_name}' error: {g_leg_err}")
            except Exception as g_leg_imp_err:
                logger.warning(f"❌ [LLM ROUTE C IMPORT FAILED] google.generativeai import error: {g_leg_imp_err}")
        except Exception as api_err:
            logger.warning(f"❌ [LLM DIRECT FALLBACK FAILED] Error: {api_err}")

    logger.warning("⚠️ [LLM OFFLINE FALLBACK] All online Gemini LLM routes failed or key invalid. Using grounded offline generator.")

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
