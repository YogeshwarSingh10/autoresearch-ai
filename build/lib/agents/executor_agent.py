import os
from openai import OpenAI

from memory.memory_manager import search_memory


# Groq API client
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def format_papers(papers):

    formatted = ""

    for i, paper in enumerate(papers, 1):

        authors = ", ".join(paper.get("authors", []))

        formatted += f"""
Paper {i}
Title: {paper['title']}
Authors: {authors}
Summary: {paper['summary']}
URL: {paper['url']}

"""

    return formatted


def format_memory(memory_hits):

    formatted = ""

    for i, item in enumerate(memory_hits, 1):

        formatted += f"""
Memory Paper {i}
Title: {item['metadata']['title']}
Summary: {item['text']}
URL: {item['metadata']['url']}

"""

    return formatted


def executor_agent(papers):

    papers_text = format_papers(papers)

    # -------------------------
    # MEMORY RETRIEVAL
    # -------------------------

    query = papers[0]["title"] if papers else ""
    memory_hits = search_memory(query)[:2] if query else []

    print(f"\nExecutor memory hits: {len(memory_hits)}\n")
    memory_text = format_memory(memory_hits) if memory_hits else ""

    # -------------------------

    system_prompt = """
You are a Research Analysis Agent in a multi-agent research system.

Your task is to analyze academic papers and produce structured research insights.

You must produce:

1. Literature Review
2. Comparison Table
3. Key Insights
4. Research Gaps

Use both the retrieved papers and memory papers if useful.
"""

    user_prompt = f"""
Analyze the following papers.

Retrieved Papers:
{papers_text}

Relevant Memory Papers:
{memory_text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0.2,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    return response.choices[0].message.content