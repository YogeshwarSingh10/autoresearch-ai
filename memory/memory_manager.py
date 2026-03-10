import uuid

from memory.embeddings import get_embedding
from memory.vector_store import VectorStore


class MemoryManager:

    def __init__(self):

        self.vector_db = VectorStore(embedding_dimension=384)

    def store_paper(self, paper):

        # text = paper["title"] + " " + paper["summary"]

        # metadata = {
        #     "title": paper["title"],
        #     "url": paper["url"]
        # }

        # self.vector_db.add(text, metadata)
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
        self.vector_db.add_documents([document], [embedding])

    def store_many(self, papers):

        # for paper in papers:
        #     self.store_paper(paper)
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
        
        self.vector_db.add_documents(documents, embeddings)

    def search(self, query, k=3):
        query_embedding = get_embedding(query)
        return self.vector_db.search(query_embedding, top_k=k)

    def reset(self):

        self.vector_db.reset()