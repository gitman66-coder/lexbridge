import ollama


MODEL_NAME = "nomic-embed-text"


def generate_embedding(text: str) -> list[float]:
    response = ollama.embed(
        model=MODEL_NAME,
        input=text
    )

    return response["embeddings"][0]
