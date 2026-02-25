from services.embedding import embed_text
from services.retrieval import retrieve_top_k
from services.llm import generate_answer

def answer_question(question: str):
    query_vector = embed_text(question)

    context_chunks = retrieve_top_k(query_vector, k=2)
    if not context_chunks:
        return {
            "answer": "I don't know.",
            "sources": []
        }

    context_text = "\n".join(context_chunks)

    prompt = f"""
    Answer ONLY from the context below.
    If the answer is not in the context, say "I don't know."

    Context:
    {context_text}

    Question:
    {question}

    Answer:
    """

    answer = generate_answer(prompt)

    return {
        "answer": answer,
        "sources": context_chunks
    }
