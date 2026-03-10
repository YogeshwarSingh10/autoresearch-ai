import os
import json
from openai import OpenAI

from memory.memory_manager import MemoryManager
from tools.search import search_arxiv
from utils.logging import setup_logging

logger = setup_logging(__name__)

RETRIEVAL_THRESHOLD=0.65

# Groq API client
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
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


def retriever_agent(planner_output, memory: MemoryManager):

    print("\nExtracting search queries...\n")

    queries = extract_queries(planner_output)

    print("Queries:", queries)

    if not queries:
        print("No queries extracted.")
        return []

    all_papers = []

    for query in queries[:5]:

        print(f"\nProcessing query: {query}\n")
        memory_hits = memory.search(query)

        print("Searching in memory: ")
        for m in memory_hits:
            logger.debug(
                f"Score: {m['score']:.4f} | Title: {m['title']}"
            )

        memory_hits = [m for m in memory_hits if m["score"] > RETRIEVAL_THRESHOLD]
        print(f"Valid Memory hits: {len(memory_hits)}")

        if memory_hits:
            print("Found relevant papers in memory")
            papers = [
                {
                    "title": m["title"],
                    "summary": m["content"],
                    "url": m["source"]
                }
                for m in memory_hits
            ]
        else:
            print("\nSearching arXiv")
            papers = search_arxiv(query, max_results=2)
            logger.debug(f"arXiv results for query: '{query}'")
            for p in papers:
                logger.debug(f"arXiv Title: {p['title']}")
            memory.store_many(papers)

        for p in papers:
            if p["url"] not in {x["url"] for x in all_papers}:
                all_papers.append(p)

    return all_papers