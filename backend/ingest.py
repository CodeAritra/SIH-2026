"""
Ingestion & Chunker Module for IP-SAKTI Sahayak (LangChain Powered).
Splits legal texts by Section/Article boundaries into LangChain Document objects
and uploads metadata vectors directly to Qdrant Cloud Vector Database.
"""

import os
import re
import json
import logging
from typing import List, Dict, Any

from langchain_core.documents import Document
from dotenv import load_dotenv

# Automatically locate and load root .env
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(dotenv_path=dotenv_path)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CORPUS_DIR = os.path.join(os.path.dirname(__file__), "..", "corpus")

def compute_simple_embedding(text: str) -> List[float]:
    """Generates a normalized bag-of-words / hash embedding vector of size 128."""
    vec = [0.0] * 128
    words = re.findall(r'\w+', text.lower())
    for word in words:
        idx = hash(word) % 128
        vec[idx] += 1.0
    norm = sum(x*x for x in vec) ** 0.5
    if norm > 0:
        vec = [x / norm for x in vec]
    return vec

def chunk_document_to_langchain(file_path: str, filename: str) -> List[Document]:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract header metadata
    title_match = re.search(r'^#\s*(.+)$', content, re.MULTILINE)
    jurisdiction_match = re.search(r'Jurisdiction:\s*(\w+)', content, re.IGNORECASE)
    ip_type_match = re.search(r'IP Type:\s*(\w+)', content, re.IGNORECASE)
    formulation_match = re.search(r'Formulation Category:\s*(.+)$', content, re.MULTILINE | re.IGNORECASE)

    source_title = title_match.group(1).strip() if title_match else filename
    jurisdiction = jurisdiction_match.group(1).strip().lower() if jurisdiction_match else "india"
    ip_type = ip_type_match.group(1).strip().lower() if ip_type_match else "patent"
    formulation_category = formulation_match.group(1).strip().lower() if formulation_match else "all"

    # Split by Section or Article markers
    section_splits = re.split(r'(?=\n(?:Section|Article)\s+\d+)', content)

    documents = []
    chunk_index = 0
    for split_text in section_splits:
        clean_text = split_text.strip()
        if not clean_text or clean_text.startswith("#") or clean_text.startswith("Jurisdiction"):
            continue

        # Extract specific section header (e.g. "Section 3(p)" or "Article 27")
        header_match = re.search(r'^(?:Section|Article)\s+[\w\(\)]+', clean_text)
        source_section = header_match.group(0) if header_match else f"Section {chunk_index + 1}"

        chunk_id = f"{filename}_chunk_{chunk_index}"
        embedding = compute_simple_embedding(clean_text)

        doc = Document(
            page_content=clean_text,
            metadata={
                "chunk_id": chunk_id,
                "source_title": source_title,
                "source_section": source_section,
                "jurisdiction": jurisdiction,
                "ip_type": ip_type,
                "formulation_category": formulation_category,
                "filename": filename,
                "embedding": embedding
            }
        )
        documents.append(doc)
        chunk_index += 1

    return documents

def ingest_corpus() -> Dict[str, Any]:
    # Ensure seed corpus is generated
    from seed_corpus import generate_seed_corpus
    if not os.path.exists(CORPUS_DIR) or len(os.listdir(CORPUS_DIR)) == 0:
        generate_seed_corpus()

    all_docs: List[Document] = []
    for fname in os.listdir(CORPUS_DIR):
        if fname.endswith(".txt"):
            fpath = os.path.join(CORPUS_DIR, fname)
            docs = chunk_document_to_langchain(fpath, fname)
            all_docs.extend(docs)

    logger.info(f"Chunked {len(all_docs)} LangChain Document objects from {len(os.listdir(CORPUS_DIR))} files.")

    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_key = os.getenv("QDRANT_API_KEY")

    if not qdrant_url or not qdrant_key:
        qdrant_status = (
            "QDRANT_URL or QDRANT_API_KEY environment variable missing in .env. "
            "Please provide Qdrant Cloud credentials in .env to upload vectors to Qdrant Cloud vector database."
        )
        logger.warning(qdrant_status)
        return {
            "status": "warning",
            "total_chunks": len(all_docs),
            "vector_store": "Qdrant Cloud",
            "qdrant_status": qdrant_status
        }

    try:
        from qdrant_client import QdrantClient
        from langchain_qdrant import QdrantVectorStore
        from langchain_community.embeddings import FakeEmbeddings

        client = QdrantClient(url=qdrant_url, api_key=qdrant_key)
        embeddings = FakeEmbeddings(size=128)
        
        qdrant_store = QdrantVectorStore.from_documents(
            documents=all_docs,
            embedding=embeddings,
            url=qdrant_url,
            api_key=qdrant_key,
            collection_name="ayush_ip_corpus_langchain"
        )

        try:
            from qdrant_client.models import PayloadSchemaType
            client.create_payload_index(
                collection_name="ayush_ip_corpus_langchain",
                field_name="metadata.jurisdiction",
                field_schema=PayloadSchemaType.KEYWORD
            )
        except Exception as idx_err:
            logger.debug(f"Qdrant payload index creation note: {idx_err}")

        qdrant_status = f"Successfully uploaded {len(all_docs)} LangChain Document vectors directly to Qdrant Cloud collection 'ayush_ip_corpus_langchain'."
        logger.info(qdrant_status)
        return {
            "status": "success",
            "total_chunks": len(all_docs),
            "vector_store": "Qdrant Cloud Managed Vector DB",
            "qdrant_status": qdrant_status
        }
    except Exception as e:
        qdrant_status = f"Qdrant Cloud connection failed ({str(e)})."
        logger.error(qdrant_status)
        return {
            "status": "error",
            "total_chunks": len(all_docs),
            "vector_store": "Qdrant Cloud",
            "qdrant_status": qdrant_status
        }

if __name__ == "__main__":
    result = ingest_corpus()
    print(json.dumps(result, indent=2))
