from schemas import PlannerOutput

def run_planner(topic, client):

    prompt = f"""
You are a research planner.

Break this topic into 4 research questions:

Topic: {topic}
"""

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )

    questions = completion.choices[0].message.content.split("\n")

    return PlannerOutput(topic, questions)