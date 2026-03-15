# 💹 Pricing Intelligence Dashboard

[![Live Demo](https://competitor-pricing-scraper-c2ofapncptttfqperzapdz.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red?style=for-the-badge&logo=streamlit)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-5.20+-blue?style=for-the-badge&logo=plotly)](https://plotly.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

> A full-featured pricing intelligence dashboard — scrape, filter, analyse, and export live e-commerce product data. Built as a portfolio-ready showcase of **web scraping**, **data analytics**, and **interactive visualisation** skills.

**🔗 Live Demo:** https://competitor-pricing-scraper-c2ofapncptttfqperzapdz.streamlit.app/

---

## ✨ Features

### 🔍 Scraping
- **Default Scraper** — scrape up to 50 pages (1,000 books) from [books.toscrape.com](http://books.toscrape.com) instantly
- **Category Scraper** — browse and scrape any of 29 genre categories (Mystery, Fantasy, Thriller, Science Fiction, and more)
- **Custom URL Scraper** — paste any compatible listing URL; `https://` is added automatically if omitted
- **Multi-page category support** — automatically follows pagination within categories

### 📊 Dashboard & Visualisation
- Bar chart — top 25 books by price
- Histogram — price frequency distribution
- Average price by star rating
- Price bucket donut chart — segment books into price ranges
- Rating distribution pie chart
- Price vs Rating scatter plot — bubble sized by Value Score

### 🔬 Analytics
- **Top 10 Best Value** books — ranked by Value Score `(Rating ÷ Price) × 10`
- **Price Trend** across pages — line chart showing avg price per scraped page
- **Auto Insights** — 5 automatically generated data insights

### 🎛️ Filters (Sidebar)
- 🔍 Search by title keyword
- 💷 Price range slider
- ⭐ Minimum star rating filter
- 📦 Availability filter
- ↕️ Sort by Price, Rating, Value Score, or Title (asc/desc)

### 📤 Export
- Download filtered data as **CSV**
- Download filtered data as **Excel (.xlsx)**

### 🎨 UI / UX
- 🌙 Dark / ☀️ Light mode toggle
- Custom typography (Syne + DM Mono fonts)
- Fully responsive wide layout
- Built-in **How to Use** guide tab

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Dashboard | Streamlit 1.35+ |
| Scraping | Requests + BeautifulSoup4 |
| Data Processing | Pandas |
| Visualisation | Plotly Express + Graph Objects |
| Excel Export | OpenPyXL |
| Language | Python 3.10+ |

---

## 📁 Project Structure

```
competitor-pricing-scraper/
│
├── app.py                   # Main Streamlit dashboard (v2.0)
├── scraper.py               # Core scraping logic
├── main.py                  # CLI entry point
├── requirements.txt
├── README.md
│
├── data/                    # CSV / Excel outputs (auto-created)
└── assets/                  # Screenshots / demo images
```

---

## 🚀 Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/IrfanaAslam/competitor-pricing-scraper.git
cd competitor-pricing-scraper
```

### 2. Create & activate a virtual environment *(recommended)*

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the dashboard

```bash
python -m streamlit run app.py
```

Open the URL shown in your terminal — usually `http://localhost:8501`.

---

## 🖥️ CLI Usage

Run the scraper headlessly from the command line and save results to CSV:

```bash
python main.py               # Scrape 5 pages (default)
python main.py --pages 10    # Scrape 10 pages
```

Output is saved to `data/competitor_prices.csv`.

---

## 💡 Value Score Explained

Every book is assigned a **Value Score**:

```
Value Score = (Star Rating ÷ Price) × 10
```

| Example | Price | Rating | Value Score |
|---|---|---|---|
| Hidden gem | £5.00 | ⭐⭐⭐⭐⭐ | **10.0** |
| Average | £20.00 | ⭐⭐⭐ | **1.5** |
| Poor value | £50.00 | ⭐⭐ | **0.4** |

Use the **Top 10 Best Value** table in the Analytics tab to find the highest-scoring books instantly.

---

## 🗂️ Category URLs (Custom URL Tab)

You can also paste these directly into the **Custom URL** tab:

```
# Genre categories
http://books.toscrape.com/catalogue/category/books/mystery_3/index.html
http://books.toscrape.com/catalogue/category/books/science-fiction_16/index.html
http://books.toscrape.com/catalogue/category/books/thriller_37/index.html
http://books.toscrape.com/catalogue/category/books/fantasy_19/index.html
http://books.toscrape.com/catalogue/category/books/romance_8/index.html
http://books.toscrape.com/catalogue/category/books/history_32/index.html
http://books.toscrape.com/catalogue/category/books/business_35/index.html
http://books.toscrape.com/catalogue/category/books/self-help_41/index.html

# Specific pages
http://books.toscrape.com/catalogue/page-1.html
http://books.toscrape.com/catalogue/page-2.html
```

---

## 📝 Usage Notes

- All scraping targets [books.toscrape.com](http://books.toscrape.com) — a **legal, purpose-built scraping sandbox**.
- Always check a site's `robots.txt` and Terms of Service before scraping any real website.
- For JavaScript-heavy sites, Selenium integration can be added (requires ChromeDriver or `webdriver-manager`).
- Be respectful — the scraper includes a polite delay between requests.

---

## 🔧 Customisation & Extension Ideas

| Idea | Description |
|---|---|
| 📧 Price alerts | Email / Telegram notifications when prices drop |
| ⏰ Scheduled scraping | GitHub Actions workflow to refresh data nightly |
| 🗄️ Database storage | SQLite / PostgreSQL for historical price tracking |
| 🎨 CSS selector input | Let users enter custom selectors for a universal scraper |
| 🚀 Auto-deploy CI | GitHub Actions pipeline to deploy to Streamlit Cloud on push |
| 📊 Price history charts | Track how prices change over time with stored snapshots |

---

## 👩‍💻 About Me

**Irfana Aslam** — Python developer & data enthusiast.
I build practical tools combining web scraping, data processing, and interactive dashboards to turn raw data into actionable business insights.

- 📧 **Email:** irfanaaslam69@gmail.com
- 🐙 **GitHub:** [github.com/IrfanaAslam](https://github.com/IrfanaAslam)
- 💼 **LinkedIn:** [linkedin.com/in/irfanaaslam](https://www.linkedin.com/in/irfanaaslam)

---

## 📄 License

This project is released under the [MIT License](LICENSE).

---

## 💬 Contact / Demo Requests

Want a tailored demo — e.g. scrape a specific competitor site, add price-change alerts, or deploy to the cloud?
Open an [issue](https://github.com/IrfanaAslam/competitor-pricing-scraper/issues) or email **irfanaaslam69@gmail.com** and I'll help you customise and deploy it.
