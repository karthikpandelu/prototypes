import ollama

def generate_answer(prompt: str) -> str:
    response = ollama.chat(
        model="llama3.1:8b",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]
