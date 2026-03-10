import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class VectorStore:

    def __init__(self):

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        dim = 384
        self.index = faiss.IndexFlatL2(dim)

        self.documents = []

    def add(self, text, metadata):

        embedding = self.model.encode([text])[0]

        self.index.add(np.array([embedding]).astype("float32"))

        self.documents.append({
            "text": text,
            "metadata": metadata
        })

    def search(self, query, k=3):

        if len(self.documents) == 0:
            return []

        query_embedding = self.model.encode([query])[0]

        distances, indices = self.index.search(
            np.array([query_embedding]).astype("float32"),
            k
        )

        results = []

        for i in indices[0]:

            if i < 0 or i >= len(self.documents):
                continue

            results.append(self.documents[i])

        return results

    def reset(self):
        self.index.reset()
        self.documents = []