from services.embedding import embed_batch
from services.retrieval import get_connection

def chunk_text(text: str, chunk_size: int = 200, overlap: int = 50):
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = words[start:end]
        chunks.append(" ".join(chunk))
        start = end - overlap

    return chunks


def ingest_document(document_id: str, source: str, content: str):
    conn = get_connection()
    cursor = conn.cursor()

    # Step 1: Delete old chunks
    cursor.execute(
        "DELETE FROM documents WHERE document_id = %s",
        (document_id,)
    )

    # Step 2: Chunk
    chunks = chunk_text(content)
    embeddings = embed_batch(chunks)

    for chunk, embedding in zip(chunks, embeddings):
        vector_str = str([float(x) for x in embedding])

        cursor.execute(
            """
            INSERT INTO documents (content, embedding, document_id, source)
            VALUES (%s, %s::vector, %s, %s)
            """,
            (chunk, vector_str, document_id, source)
        )

    conn.commit()
    cursor.close()
    conn.close()
