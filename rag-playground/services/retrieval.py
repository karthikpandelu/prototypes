import psycopg2
from typing import List

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

    cursor.close()
    conn.close()

    if not results or results[0][1] > 0.5:
        return []
    return [row[0] for row in results]
