import os
from openai import OpenAI

from memory.memory_manager import MemoryManager


# Groq API client
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

EXECUTOR_THRESHOLD=0.65

def format_papers(papers):

    lines = []

    for i, paper in enumerate(papers, 1):

        authors = ", ".join(paper.get("authors", []))

        lines.append(
            f"""
Paper {i}
Title: {paper['title']}
Authors: {authors}
Summary: {paper['summary']}
URL: {paper['url']}
"""
        )

    return "\n".join(lines)


def format_memory(memory_hits):
    formatted = ""
    for i, item in enumerate(memory_hits, 1):
        formatted += f"""
Memory Paper {i}
Title: {item['title']}
Summary: {item['content']}
URL: {item['source']}
"""
    return formatted


def executor_agent(papers, memory: MemoryManager):

    papers_text = format_papers(papers)

    # -------------------------
    # MEMORY RETRIEVAL
    # -------------------------

    query = papers[0]["title"] if papers else ""
    memory_hits = [m for m in memory.search(query) if m["score"] > EXECUTOR_THRESHOLD][:2] if query else []

    print(f"\nExecutor memory hits: {len(memory_hits)}\n")
    memory_text = format_memory(memory_hits) if memory_hits else ""

    # -------------------------

    system_prompt = """
    You are a Research Analysis Agent in a multi-agent research system.
    
    Your role is to deeply analyze academic papers and extract structured insights.
    
    Produce a detailed analysis with the following sections:
    
    1. Paper Summaries
       - 3-5 sentence explanation of each paper's key idea and contribution.
    
    2. Literature Themes
       - Identify major approaches or categories across papers.
    
    3. Method Comparison
        Return a markdown table with columns:
        | Paper | Method | Dataset | Strength | Limitation |
    
    4. Key Insights
       - Important takeaways emerging from the literature.
    
    5. Research Gaps
       - Missing work, unresolved challenges, or limitations.
    
    Important rules:
    - Use evidence from the papers.
    - Avoid repeating the same information.
    - Focus on synthesis, not just restating summaries.
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