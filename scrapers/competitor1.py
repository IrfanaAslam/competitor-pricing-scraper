import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_competitor1():
    url = "https://quotes.toscrape.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []

    for quote in soup.select(".quote"):
        text = quote.select_one(".text").text
        author = quote.select_one(".author").text

        results.append({
            "Competitor": "QuotesToScrape",
            "Product Name": text,
            "Price": "N/A",
            "Stock Status": author,
            "Scraped At": datetime.now()
        })

    return results
