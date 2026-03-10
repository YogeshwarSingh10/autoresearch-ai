import os
import json
from openai import OpenAI

from memory.memory_manager import store_many, search_memory
from tools.search import search_arxiv


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


def retriever_agent(planner_output):

    print("\nExtracting search queries...\n")

    queries = extract_queries(planner_output)

    print("Queries:", queries)

    if not queries:
        print("No queries extracted.")
        return []

    all_papers = []

    for query in queries[:5]:

        print(f"\nProcessing query: {query}\n")

        # STEP 1 — check memory
        memory_hits = search_memory(query)

        print(f"Memory hits: {len(memory_hits)}")

        if memory_hits:
            print("Found papers in memory")

            papers = [
                {
                    "title": m["metadata"]["title"],
                    "summary": m["text"],
                    "url": m["metadata"]["url"]
                }
                for m in memory_hits
            ]

        else:
            print("Searching arXiv")

            papers = search_arxiv(query, max_results=2)

            # STEP 2 — store new papers in memory
            store_many(papers)

        for p in papers:
            if p["url"] not in {x["url"] for x in all_papers}:
                all_papers.append(p)

    return all_papers