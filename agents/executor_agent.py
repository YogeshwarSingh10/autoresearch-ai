from openai import OpenAI

# Groq API client
client = OpenAI(
    api_key="key",
    base_url="https://api.groq.com/openai/v1"
)


def format_papers(papers):
    """
    Convert paper metadata into readable text for the LLM
    """

    formatted = ""

    for i, paper in enumerate(papers, 1):

        formatted += f"""
Paper {i}
Title: {paper['title']}
Authors: {", ".join(paper['authors'])}
Summary: {paper['summary']}
URL: {paper['url']}

"""

    return formatted


def executor_agent(papers):

    papers_text = format_papers(papers)

    system_prompt = """
You are a Research Analysis Agent in a multi-agent research system.

Your task is to analyze academic papers and produce structured research insights.

You must produce:

1. Literature Review
   - summarize the key approaches across papers

2. Comparison Table
   Columns:
   - Paper
   - Method
   - Dataset
   - Key Contribution

3. Key Insights
   - important trends or patterns

4. Research Gaps
   - what problems remain unsolved
"""

    user_prompt = f"""
Analyze the following papers and produce the required outputs.

Papers:
{papers_text}
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

