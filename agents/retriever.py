from schemas import RetrievalResult
from tools.search import search
from tools.scrape import scrape
from tools.summarize import summarize

def run_retriever(question):

    urls = search(question)

    summaries = []

    for url in urls:
        text = scrape(url)
        summaries.append(summarize(text))

    return RetrievalResult(question, urls, summaries)