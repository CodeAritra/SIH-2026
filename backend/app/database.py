"""
SQLite Database Layer for IP-SAKTI Sahayak.
Handles audit logging of user queries, citations, confidence scores, human escalations, and evaluation metrics.
"""

import os
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

DB_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
DB_PATH = os.path.join(DB_DIR, "ipsakti.db")

def init_db():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Query audit logs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS query_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        session_id TEXT,
        user_query TEXT NOT NULL,
        jurisdiction TEXT NOT NULL,
        classification TEXT,
        retrieved_chunks TEXT NOT NULL,
        llm_raw_answer TEXT NOT NULL,
        citations TEXT NOT NULL,
        confidence TEXT NOT NULL,
        is_blocked BOOLEAN NOT NULL,
        abs_triggered BOOLEAN NOT NULL,
        tkdl_triggered BOOLEAN NOT NULL
    )
    """)

    # Escalations table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS escalations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        user_query TEXT NOT NULL,
        product_category TEXT,
        jurisdiction TEXT NOT NULL,
        notes TEXT,
        status TEXT DEFAULT 'Pending'
    )
    """)

    # Evaluation Runs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS eval_runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        run_name TEXT NOT NULL,
        total_queries INTEGER NOT NULL,
        precision_at_k REAL NOT NULL,
        recall_at_k REAL NOT NULL,
        mrr REAL NOT NULL,
        citation_validity_rate REAL NOT NULL,
        abstention_rate REAL NOT NULL,
        details_json TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

def log_query(
    session_id: str,
    user_query: str,
    jurisdiction: str,
    classification: Optional[str],
    retrieved_chunks: List[Dict[str, Any]],
    llm_raw_answer: str,
    citations: List[Dict[str, Any]],
    confidence: str,
    is_blocked: bool,
    abs_triggered: bool,
    tkdl_triggered: bool
) -> int:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    timestamp = datetime.utcnow().isoformat()
    cursor.execute("""
    INSERT INTO query_logs (
        timestamp, session_id, user_query, jurisdiction, classification,
        retrieved_chunks, llm_raw_answer, citations, confidence,
        is_blocked, abs_triggered, tkdl_triggered
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        timestamp, session_id, user_query, jurisdiction, classification,
        json.dumps(retrieved_chunks), llm_raw_answer, json.dumps(citations),
        confidence, is_blocked, abs_triggered, tkdl_triggered
    ))
    
    log_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return log_id

def log_escalation(
    name: str,
    email: str,
    user_query: str,
    product_category: Optional[str],
    jurisdiction: str,
    notes: Optional[str] = None
) -> int:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    timestamp = datetime.utcnow().isoformat()
    cursor.execute("""
    INSERT INTO escalations (timestamp, name, email, user_query, product_category, jurisdiction, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (timestamp, name, email, user_query, product_category, jurisdiction, notes))
    
    esc_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return esc_id

def log_eval_run(
    run_name: str,
    total_queries: int,
    precision_at_k: float,
    recall_at_k: float,
    mrr: float,
    citation_validity_rate: float,
    abstention_rate: float,
    details: List[Dict[str, Any]]
) -> int:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    timestamp = datetime.utcnow().isoformat()
    cursor.execute("""
    INSERT INTO eval_runs (
        timestamp, run_name, total_queries, precision_at_k, recall_at_k, mrr,
        citation_validity_rate, abstention_rate, details_json
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        timestamp, run_name, total_queries, precision_at_k, recall_at_k, mrr,
        citation_validity_rate, abstention_rate, json.dumps(details)
    ))
    
    run_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return run_id

def get_latest_eval_runs(limit: int = 5) -> List[Dict[str, Any]]:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT id, timestamp, run_name, total_queries, precision_at_k, recall_at_k, mrr,
           citation_validity_rate, abstention_rate, details_json
    FROM eval_runs ORDER BY id DESC LIMIT ?
    """, (limit,))
    
    rows = cursor.fetchall()
    conn.close()
    
    runs = []
    for r in rows:
        runs.append({
            "id": r[0],
            "timestamp": r[1],
            "run_name": r[2],
            "total_queries": r[3],
            "precision_at_k": r[4],
            "recall_at_k": r[5],
            "mrr": r[6],
            "citation_validity_rate": r[7],
            "abstention_rate": r[8],
            "details": json.loads(r[9])
        })
    return runs

def get_query_logs(limit: int = 20) -> List[Dict[str, Any]]:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT id, timestamp, session_id, user_query, jurisdiction, classification,
           retrieved_chunks, llm_raw_answer, citations, confidence, is_blocked,
           abs_triggered, tkdl_triggered
    FROM query_logs ORDER BY id DESC LIMIT ?
    """, (limit,))
    
    rows = cursor.fetchall()
    conn.close()
    
    logs = []
    for r in rows:
        logs.append({
            "id": r[0],
            "timestamp": r[1],
            "session_id": r[2],
            "user_query": r[3],
            "jurisdiction": r[4],
            "classification": r[5],
            "retrieved_chunks": json.loads(r[6]),
            "llm_raw_answer": r[7],
            "citations": json.loads(r[8]),
            "confidence": r[9],
            "is_blocked": bool(r[10]),
            "abs_triggered": bool(r[11]),
            "tkdl_triggered": bool(r[12])
        })
    return logs
