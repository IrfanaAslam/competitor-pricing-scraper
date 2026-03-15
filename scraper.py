"""
scraper.py — Core scraping logic for Competitor Pricing Scraper (v2).
Place this file in the same folder as app.py.
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

CATEGORIES = {
    "Travel": "travel_2",
    "Mystery": "mystery_3",
    "Historical Fiction": "historical-fiction_4",
    "Classics": "classics_6",
    "Philosophy": "philosophy_7",
    "Romance": "romance_8",
    "Fiction": "fiction_10",
    "Childrens": "childrens_11",
    "Nonfiction": "nonfiction_13",
    "Science Fiction": "science-fiction_16",
    "Sports and Games": "sport_17",
    "Fantasy": "fantasy_19",
    "Young Adult": "young-adult_21",
    "Science": "science_22",
    "Poetry": "poetry_23",
    "Art": "art_25",
    "Psychology": "psychology_26",
    "Autobiography": "autobiography_27",
    "Humor": "humor_30",
    "Horror": "horror_31",
    "History": "history_32",
    "Food and Drink": "food-and-drink_33",
    "Biography": "biography_34",
    "Business": "business_35",
    "Thriller": "thriller_37",
    "Self Help": "self-help_41",
    "Health": "health_47",
    "Politics": "politics_48",
    "Crime": "crime_51",
}


def parse_books_from_soup(soup: BeautifulSoup, page_num: int = 1) -> list:
    """Extract book data from a parsed page soup."""
    books = []
    for book in soup.select("article.product_pod"):
        try:
            title = book.h3.a["title"]
            price_text = book.select_one("p.price_color").text
            price = float(
                price_text.replace("£", "")
                          .replace("Â", "")
                          .replace("\xa3", "")
                          .strip()
            )
            availability = book.select_one("p.instock.availability").text.strip()
            rating_word = book.select_one("p.star-rating")["class"][1]
            rating = RATING_MAP.get(rating_word, 0)
            value_score = round(rating / price * 10, 2) if price > 0 else 0

            books.append({
                "Title": title,
                "Price (£)": price,
                "Rating (Stars)": rating,
                "Availability": availability,
                "Value Score": value_score,
                "Page": page_num,
            })
        except Exception:
            continue
    return books


def scrape_books(num_pages: int = 5, delay: float = 0.3) -> pd.DataFrame:
    """Scrape books from books.toscrape.com across multiple pages."""
    num_pages = min(num_pages, 50)
    all_books = []

    for page in range(1, num_pages + 1):
        url = BASE_URL.format(page)
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"⚠️  Page {page} failed: {e}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        books = parse_books_from_soup(soup, page_num=page)
        all_books.extend(books)
        print(f"✅ Page {page}/{num_pages} — {len(books)} books scraped")
        time.sleep(delay)

    df = pd.DataFrame(all_books)
    if not df.empty:
        df.drop_duplicates(subset="Title", inplace=True)
        df.reset_index(drop=True, inplace=True)
    return df


def scrape_custom_url(url: str) -> pd.DataFrame:
    """Scrape books from any compatible URL. Auto-adds https:// if missing."""
    url = url.strip()
    if url and not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"⚠️  Failed to fetch URL: {e}")
        return pd.DataFrame()

    soup = BeautifulSoup(response.text, "html.parser")
    books = parse_books_from_soup(soup)
    return pd.DataFrame(books)


def scrape_category(category_slug: str) -> pd.DataFrame:
    """Scrape all books from a specific category (handles multi-page categories)."""
    base = f"http://books.toscrape.com/catalogue/category/books/{category_slug}/index.html"
    all_books = []
    page = 1

    while True:
        url = base if page == 1 else base.replace("index.html", f"page-{page}.html")
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 404:
                break
            response.raise_for_status()
        except requests.RequestException:
            break

        soup = BeautifulSoup(response.text, "html.parser")
        books = parse_books_from_soup(soup, page_num=page)
        if not books:
            break
        all_books.extend(books)
        print(f"✅ Category page {page} — {len(books)} books")
        page += 1
        time.sleep(0.3)

    df = pd.DataFrame(all_books)
    if not df.empty:
        df.drop_duplicates(subset="Title", inplace=True)
        df.reset_index(drop=True, inplace=True)
    return df
