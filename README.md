# 🛒 Competitor Pricing Scraper

[![Live Demo](https://img.shields.io/badge/Live-Demo-Streamlit-blue?style=for-the-badge&logo=streamlit)]
[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)](https://www.python.org/)  
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

# About the Project

**Competitor Pricing Scraper** is an interactive Streamlit dashboard that scrapes product prices from e-commerce pages and visualizes pricing insights. It’s built to be a portfolio-ready demo showing **web scraping**, **data cleaning**, and **interactive visualization** skills.

**Live demo:**  
https://competitor-pricing-scraper-c2ofapncptttfqperzapdz.streamlit.app/

---

## Features

- ✅ Default scraper (Books to Scrape) for instant demo data  
- ✅ User-input scraper: paste a product/category URL and scrape results  
- ✅ Clean price parsing and NaN handling  
- ✅ Interactive charts (Plotly) and searchable product table  
- ✅ Price-range filter and exportable CSV (download button)  
- ✅ Modular scrapers (Requests + BeautifulSoup) with optional Selenium support for dynamic sites

---

## Tech Stack

- **Python 3.10+**  
- **Streamlit** (dashboard)  
- **Requests + BeautifulSoup** (scraping static pages)  
- **Selenium** (optional, dynamic pages)  
- **Pandas** (data processing)  
- **Plotly** (interactive visualizations)

---

## Repo Structure

competitor-pricing-scraper/
│
├─ app.py # Main Streamlit dashboard
├─ scraper.py # Example scraper (books / webscraper test site)
├─ scrapers/ # Additional scraper modules (books_scraper.py, etc.)
├─ utils/ # helpers (email alerts, cleaning utilities)
├─ assets/ # screenshots / demo images
├─ requirements.txt
└─ README.md

yaml
Copy code

---

## Quick Start (Run locally)

1. Clone:

git clone https://github.com/yourusername/competitor-pricing-scraper.git
cd competitor-pricing-scraper
Create & activate venv (recommended):

bash
Copy code
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Run the app:

bash
Copy code
python -m streamlit run app.py
Open the URL shown in the terminal (usually http://localhost:8501).

## Usage Notes
The default demo scrapes books.toscrape.com (safe demo site).

To scrape other sites, paste a product/category URL into the Custom URL tab. For sites that load data with JavaScript you may need the Selenium option (setup ChromeDriver or use webdriver-manager).

Do not scrape sites you don't have permission to scrape or that block automated access; check each site's robots.txt / terms of service.


## Customization & Extensions (ideas to impress)
Add email / Telegram alerts for price changes (utils/email_alert.py)

Add scheduled scraping via GitHub Actions to update data nightly

Add a Streamlit Cloud deployment badge and CI (GitHub Actions) to auto-deploy on push

Add selector input: let users type CSS selectors for Name / Price to make the scraper universal

## About Me
Irfana Aslam — Python developer & data enthusiast.
I build practical tools combining web scraping, data processing, and interactive dashboards to turn raw data into business insights.

Email: irfanaaslam69@gmail.com

GitHub: https://github.com/IrfanaAslam

LinkedIn: https://www.linkedin.com/in/irfanaaslam (optional — add your profile link)

## License
This project is released under the MIT License. See LICENSE for details.

## Contact / Demo Requests
Want a tailored demo (e.g., scrape a specific competitor or add alerts)? Open an issue or contact me at irfanaaslam69@gmail.com — I’ll help you customize and deploy it.

