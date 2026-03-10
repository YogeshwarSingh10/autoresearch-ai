import requests
from bs4 import BeautifulSoup


def scrape_page(url):

    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    return soup.get_text()