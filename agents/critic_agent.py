from openai import OpenAI

# Groq API client
client = OpenAI(
    api_key="key",
    base_url="https://api.groq.com/openai/v1"
)


def critic_agent(executor_output):

    system_prompt = """
You are a Research Critic Agent in a multi-agent research system.

Your job is to review a research analysis report and improve its quality.

Evaluate the report based on:

1. Completeness
2. Logical consistency
3. Evidence from the papers
4. Clarity of explanations

Then produce:

1. Issues Found
2. Suggested Improvements
3. Revised Final Research Summary
"""

    user_prompt = f"""
Review the following research report produced by another agent.

Report:
{executor_output}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0.1,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    return response.choices[0].message.content
