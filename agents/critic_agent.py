import os
from openai import OpenAI

# Groq API client
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def critic_agent(executor_output):

    system_prompt = """
    You are a Senior Research Editor.

    Your job is to convert a raw literature analysis into a polished research report.

    Write a clear, structured, non-repetitive report.

    The report must follow this structure:

    # Research Report

    ## Topic Overview
    Brief explanation of the topic and why it matters.

    ## Key Papers
    Short description of the most important papers.

    ## Literature Review
    Synthesize the approaches and findings across papers.

    ## Method Comparison
    Provide a concise comparison of major methods.

    ## Key Insights
    Important trends and conclusions.

    ## Research Gaps
    What problems remain unsolved.

    ## Future Research Directions
    Promising directions for future work.

    ## References
    List paper titles.

    Important rules:
    - Avoid repetition
    - Write clearly
    - Focus on synthesis, not listing
    - Keep explanations concise but informative
    """

    user_prompt = f"""
    Convert the following analysis into a well-structured research report.

    Analysis:
    {executor_output}
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