import os
from openai import OpenAI

# Groq API client
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def planner_agent(research_goal):

    system_prompt = """
    You are a Research Planning Agent in a multi-agent research system.

    Your job is to convert a research goal into a structured research plan
    that other agents can execute.

    Produce the following sections:

    1. Key subtopics to investigate
    2. Search queries for academic papers
    3. Important evaluation criteria
    4. Suggested research workflow steps
    """

    user_prompt = f"""
    Research Goal:
    {research_goal}

    Create a structured research plan.
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