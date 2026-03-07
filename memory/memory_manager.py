import os
import uuid
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from memory.vector_store import VectorStore

load_dotenv()

model = SentenceTransformer("all-MiniLM-L6-v2")

vector_db = VectorStore(embedding_dimension=384)


def get_embedding(text: str) -> list[float]:
    return model.encode(text).tolist()


def store_paper(paper):
    text = f'{paper["title"]} {paper["summary"]}'

    document = {
        "id": str(uuid.uuid4()),
        "content": text,
        "title": paper["title"],
        "source": paper.get("url", ""),
        "metadata": {
            "title": paper["title"],
            "url": paper.get("url", "")
        }
    }

    embedding = get_embedding(text)
    vector_db.add_documents([document], [embedding])


def store_many(papers):
    if not papers:
        return

    documents = []
    embeddings = []

    for paper in papers:
        text = f'{paper["title"]} {paper["summary"]}'

        document = {
            "id": str(uuid.uuid4()),
            "content": text,
            "title": paper["title"],
            "source": paper.get("url", ""),
            "metadata": {
                "title": paper["title"],
                "url": paper.get("url", "")
            }
        }

        documents.append(document)
        embeddings.append(get_embedding(text))

    vector_db.add_documents(documents, embeddings)


def search_memory(query: str, top_k: int = 3):
    query_embedding = get_embedding(query)
    results = vector_db.search(query_embedding, top_k=top_k)

    formatted_results = []
    for r in results:
        formatted_results.append({
            "text": r.get("content", ""),
            "metadata": {
                "title": r.get("title", ""),
                "url": r.get("source", "")
            }
        })

    return formatted_results
