from memory.vector_store import VectorStore


class MemoryManager:

    def __init__(self):

        self.vector_db = VectorStore()

    def store_paper(self, paper):

        text = paper["title"] + " " + paper["summary"]

        metadata = {
            "title": paper["title"],
            "url": paper["url"]
        }

        self.vector_db.add(text, metadata)

    def store_many(self, papers):

        for paper in papers:
            self.store_paper(paper)

    def search(self, query, k=3):

        return self.vector_db.search(query, k)

    def reset(self):

        self.vector_db.reset()