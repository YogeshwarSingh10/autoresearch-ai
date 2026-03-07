import arxiv


def search_arxiv(query, max_results=5):

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    papers = []

    for result in search.results():
        papers.append({
            "title": result.title,
            "authors": [a.name for a in result.authors],
            "summary": result.summary,
            "published": str(result.published.date()),
            "url": result.entry_id
        })

    return papers

def web_search(query):
    # placeholder for Tavily / SerpAPI etc
    pass