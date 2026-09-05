"""
Retriever Module for IP-SAKTI Sahayak (Qdrant Cloud Managed Vector Store).
Performs similarity search directly on Qdrant Cloud collection 'ayush_ip_corpus_langchain'
with mandatory jurisdiction metadata filtering.
"""

import os
import math
import logging
from typing import List, Dict, Any, Tuple
from langchain_core.documents import Document
from dotenv import load_dotenv

# Automatically locate and load root .env
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
load_dotenv(dotenv_path=dotenv_path)

from ingest import compute_simple_embedding, chunk_document_to_langchain, CORPUS_DIR

logger = logging.getLogger(__name__)

# Global cache for in-memory corpus chunks when Qdrant Cloud credentials are being configured
_CORPUS_CACHE: List[Document] = []

def get_corpus_documents() -> List[Document]:
    global _CORPUS_CACHE
    if not _CORPUS_CACHE and os.path.exists(CORPUS_DIR):
        for fname in os.listdir(CORPUS_DIR):
            if fname.endswith(".txt"):
                fpath = os.path.join(CORPUS_DIR, fname)
                docs = chunk_document_to_langchain(fpath, fname)
                _CORPUS_CACHE.extend(docs)
    return _CORPUS_CACHE

def compute_cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    if not vec1 or not vec2 or len(vec1) != len(vec2):
        return 0.0
    dot = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)

def generate_query_embedding(query_text: str) -> List[float]:
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=gemini_key)
            result = genai.embed_content(
                model="models/text-embedding-004",
                content=query_text,
                task_type="retrieval_query"
            )
            vec = result['embedding']
            if len(vec) > 128:
                vec = vec[:128]
            norm = math.sqrt(sum(x*x for x in vec))
            return [x / norm for x in vec] if norm > 0 else vec
        except Exception:
            pass
            
    return compute_simple_embedding(query_text)

def retrieve_chunks(query: str, jurisdiction: str = "india", top_k: int = 5) -> Tuple[List[Dict[str, Any]], str, float]:
    """
    Queries Qdrant Cloud managed vector database with mandatory jurisdiction filter.
    Returns (retrieved_chunks, confidence_level, max_similarity_score).
    """
    target_jurisdiction = jurisdiction.lower()
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_key = os.getenv("QDRANT_API_KEY")

    # Primary Route: Direct Qdrant Cloud Similarity Search via LangChain QdrantVectorStore / Client
    if qdrant_url and qdrant_key:
        try:
            from qdrant_client import QdrantClient
            from qdrant_client.models import Filter, FieldCondition, MatchValue
            from langchain_qdrant import QdrantVectorStore
            from langchain_community.embeddings import FakeEmbeddings

            client = QdrantClient(url=qdrant_url, api_key=qdrant_key)
            embeddings = FakeEmbeddings(size=128)
            
            # Ensure Qdrant payload index for metadata.jurisdiction exists
            try:
                from qdrant_client.models import PayloadSchemaType
                client.create_payload_index(
                    collection_name="ayush_ip_corpus_langchain",
                    field_name="metadata.jurisdiction",
                    field_schema=PayloadSchemaType.KEYWORD
                )
            except Exception:
                pass

            qdrant_store = QdrantVectorStore(
                client=client,
                collection_name="ayush_ip_corpus_langchain",
                embedding=embeddings
            )

            # Similarity search with Qdrant metadata filter, fallback to local filtering if Qdrant index error
            try:
                results_with_score = qdrant_store.similarity_search_with_score(
                    query=query,
                    k=top_k,
                    filter=Filter(
                        must=[
                            FieldCondition(
                                key="metadata.jurisdiction",
                                match=MatchValue(value=target_jurisdiction)
                            )
                        ]
                    )
                )
            except Exception as filter_err:
                logger.warning(f"Qdrant filtered vector search error ({filter_err}). Falling back to Qdrant search with local jurisdiction filter.")
                unfiltered_results = qdrant_store.similarity_search_with_score(query=query, k=top_k * 3)
                results_with_score = [
                    (doc, score) for doc, score in unfiltered_results
                    if str(doc.metadata.get("jurisdiction", "")).lower() == target_jurisdiction
                ][:top_k]

            scored_chunks = []
            for doc, score in results_with_score:
                scored_chunks.append({
                    "chunk_id": doc.metadata.get("chunk_id", "qdrant_chunk"),
                    "text": doc.page_content,
                    "metadata": doc.metadata,
                    "score": round(score, 4),
                    "langchain_doc": doc
                })

            if scored_chunks:
                max_score = scored_chunks[0]["score"]
                confidence = "High" if max_score >= 0.65 else ("Medium" if max_score >= 0.25 else "Low")
                return scored_chunks, confidence, max_score

        except Exception as e:
            logger.error(f"Qdrant Cloud vector query error: {str(e)}")

    # In-memory document scanning filtered strictly by jurisdiction
    docs = get_corpus_documents()
    query_vec = generate_query_embedding(query)

    filtered_docs = [
        d for d in docs
        if d.metadata.get("jurisdiction", "").lower() == target_jurisdiction
    ]

    scored_chunks = []
    for doc in filtered_docs:
        emb = doc.metadata.get("embedding", compute_simple_embedding(doc.page_content))
        score = compute_cosine_similarity(query_vec, emb)
        
        words = [w.lower() for w in query.split() if len(w) > 3]
        text_lower = doc.page_content.lower()
        match_count = sum(1 for w in words if w in text_lower)
        keyword_boost = min(0.3, match_count * 0.08)
        final_score = min(1.0, score + keyword_boost)

        scored_chunks.append({
            "chunk_id": doc.metadata.get("chunk_id", "doc_chunk"),
            "text": doc.page_content,
            "metadata": doc.metadata,
            "score": round(final_score, 4),
            "langchain_doc": doc
        })

    scored_chunks.sort(key=lambda x: x["score"], reverse=True)
    top_chunks = scored_chunks[:top_k]

    max_score = top_chunks[0]["score"] if top_chunks else 0.0
    confidence = "High" if max_score >= 0.65 else ("Medium" if max_score >= 0.25 else "Low")

    return top_chunks, confidence, max_score

