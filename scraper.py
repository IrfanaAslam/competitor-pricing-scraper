import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"

def scrape_books(num_pages=2):
    products = []
    for page in range(1, num_pages + 1):
        url = BASE_URL.format(page)
        response = requests.get(url)
        if response.status_code != 200:
            continue
        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.select("article.product_pod")
        for book in books:
            title = book.h3.a["title"]
            price_text = book.select_one("p.price_color").text
            price = float(price_text.replace("£", "").replace("Â", ""))
            availability = book.select_one("p.instock.availability").text.strip()
            products.append({
                "Title": title,
                "Price (£)": price,
                "Availability": availability
            })
    return pd.DataFrame(products)
