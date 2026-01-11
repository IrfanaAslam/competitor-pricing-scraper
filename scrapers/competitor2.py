import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_competitor2():
    url = "https://example.org/shop"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    products = []

    for item in soup.find_all("div", class_="item-card"):
        name = item.find("h2").text.strip()
        price = item.find("span", class_="item-price").text.strip()
        stock = item.find("span", class_="stock").text.strip()

        products.append({
            "Competitor": "Competitor 2",
            "Product Name": name,
            "Price": price,
            "Stock Status": stock,
            "Scraped At": datetime.now()
        })

    return products
