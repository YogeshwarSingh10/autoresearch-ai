from memory.vector_store import VectorStore

vector_db = VectorStore()


def store_paper(paper):

    text = paper["title"] + " " + paper["summary"]

    metadata = {
        "title": paper["title"],
        "url": paper["url"]
    }

    vector_db.add(text, metadata)


def store_many(papers):

    for p in papers:
        store_paper(p)


def search_memory(query):

    return vector_db.search(query)