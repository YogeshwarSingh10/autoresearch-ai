import arxiv
from openai import OpenAI
import re
import json

# Groq client
client = OpenAI(
    api_key="key",
    base_url="https://api.groq.com/openai/v1"
)


def extract_queries(planner_output):
    """
    Use LLM to extract clean search queries from planner output
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0.1,
        messages=[
            {
                "role": "system",
                "content": """Extract search queries from the research plan.
Return ONLY valid JSON in this format:
{"queries": ["query1", "query2", "query3"]}"""
            },
            {
                "role": "user",
                "content": planner_output
            }
        ]
    )

    content = response.choices[0].message.content

    try:
        data = json.loads(content)
        return data.get("queries", [])
    except json.JSONDecodeError:
        print("Failed to parse queries from LLM output.")
        print("LLM Output:", content)
        return []


def search_arxiv(query, max_results=5):
    """
    Search arXiv for relevant papers
    """

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


def retriever_agent(planner_output):

    print("\nExtracting search queries...\n")

    queries = extract_queries(planner_output)

    print("Queries:", queries)

    if not queries:
        print("No queries extracted.")
        return []

    all_papers = []

    for query in queries[:5]:

        print(f"\nSearching arXiv for: {query}\n")

        papers = search_arxiv(query, max_results=2)

        all_papers.extend(papers)

    return all_papers
