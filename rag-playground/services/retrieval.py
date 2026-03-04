import psycopg2
from typing import List
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="postgres"
    )

def retrieve_top_k(query_vector, k: int = 2) -> List[str]:
    conn = get_connection()
    cursor = conn.cursor()

    vector_str = str([float(x) for x in query_vector])

    cursor.execute(
        """
        SELECT content, embedding <=> %s::vector AS distance
        FROM documents
        ORDER BY embedding <=> %s::vector
        LIMIT %s
        """,
        (vector_str, vector_str, k)
    )

    results = cursor.fetchall()

    for content, distance in results:
        logger.info(f"Retrieved chunk with distance={distance:.4f}")

    cursor.close()
    conn.close()

    if not results or results[0][1] > 0.5:
        logger.info("Top result above threshold. Returning empty.")
        return []
    return [row[0] for row in results]

def keyword_search(query: str, k: int = 3):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT content
        FROM documents
        WHERE content ILIKE %s
        LIMIT %s
        """,
        (f"%{query}%", k)
    )

    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return [row[0] for row in results]

def hybrid_retrieve(query: str, query_vector, k: int = 3):
    conn = get_connection()
    cursor = conn.cursor()

    vector_str = str([float(x) for x in query_vector])

    # Vector search
    cursor.execute(
        """
        SELECT content, embedding <=> %s::vector AS distance
        FROM documents
        ORDER BY embedding <=> %s::vector
        LIMIT %s
        """,
        (vector_str, vector_str, k)
    )
    vector_results = cursor.fetchall()

    # Keyword search
    cursor.execute(
        """
        SELECT content,
            ts_rank(content_tsv, plainto_tsquery('english', %s)) AS rank
        FROM documents
        WHERE content_tsv @@ plainto_tsquery('english', %s)
        ORDER BY rank DESC
        LIMIT %s
        """,
        (f"%{query}%", k)
    )
    keyword_results = cursor.fetchall()

    cursor.close()
    conn.close()

    # Convert to structures
    vector_dict = {content: distance for content, distance in vector_results}
    keyword_set = {row[0] for row in keyword_results}

    merged = {}

    # Add vector results
    for content, distance in vector_dict.items():
        score = distance
        if content in keyword_set:
            score -= 0.1  # boost
        merged[content] = score

    # Add keyword-only results
    for content in keyword_set:
        if content not in merged:
            merged[content] = 0.6  # moderate default distance

    # Sort by score (lower is better)
    sorted_results = sorted(merged.items(), key=lambda x: x[1])

    return sorted_results[:k]
