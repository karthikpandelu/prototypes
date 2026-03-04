from services.embedding import embed_text
from services.retrieval import retrieve_top_k
from services.llm import generate_answer
from services.retrieval import hybrid_retrieve

def answer_question(question: str):
    query_vector = embed_text(question)

    results = hybrid_retrieve(question, query_vector, k=3)
    if not results or results[0][1] > 0.4:
        return {
            "answer": "I don't know.",
            "sources": []
        }

    context_chunks = [content for content, _ in results]
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
