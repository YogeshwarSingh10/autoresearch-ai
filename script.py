import os
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
from groq import Groq

# Load keys from environment
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def search(query):
    print("\nStep 1: Searching sources...")

    results = tavily.search(query=query, max_results=5)
    urls = []

    for r in results["results"]:
        url = r["url"]
        if "reddit" not in url:
            urls.append(url)

    urls = urls[:3]

    print("Found sources:")
    for u in urls:
        print("-", u)

    return urls


def scrape(url):
    print("\nStep 2: Scraping:", url)

    html = requests.get(url, timeout=10).text
    soup = BeautifulSoup(html, "html.parser")

    text = soup.get_text()
    return text[:5000]


def summarize(text):
    print("Step 3: Summarizing content...")

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a research assistant."},
            {"role": "user", "content": f"Summarize this text:\n{text}"},
        ],
    )

    return completion.choices[0].message.content


def synthesize(summaries, topic):
    print("\nStep 4: Synthesizing research report...")

    combined = "\n\n".join(summaries)

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a research analyst."},
            {
                "role": "user",
                "content": f"""
Write a structured research report on: {topic}

Use the following summarized sources:

{combined}

Return a report with:

1. Key insights
2. Major trends
3. Important statistics
4. Final conclusion
""",
            },
        ],
    )

    return completion.choices[0].message.content


def research(query):

    urls = search(query)

    summaries = []
    sources = []

    for url in urls:
        try:
            text = scrape(url)
            summary = summarize(text)

            summaries.append(summary)
            sources.append(url)

        except Exception as e:
            print("Error processing", url, ":", e)

    report = synthesize(summaries, query)

    print("\n==============================")
    print("FINAL SYNTHESIZED REPORT")
    print("==============================\n")

    print(report)

    print("\nSources used:")
    for s in sources:
        print("-", s)


if __name__ == "__main__":

    while True:

        query = input("\nEnter research topic (or 'exit'): ")

        if query.lower() == "exit":
            break

        research(query)