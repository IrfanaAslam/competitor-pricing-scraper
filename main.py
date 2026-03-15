"""
main.py — Run the scraper from the command line and save results to CSV.
Usage:
    python main.py                   # scrape 5 pages (default)
    python main.py --pages 10        # scrape 10 pages
"""
import argparse
import os
from scraper import scrape_books

def main():
    parser = argparse.ArgumentParser(description="Competitor Pricing Scraper")
    parser.add_argument("--pages", type=int, default=5, help="Number of pages to scrape (max 50)")
    args = parser.parse_args()

    print(f"🚀 Starting scraper — {args.pages} page(s)...\n")
    df = scrape_books(num_pages=args.pages)

    if df.empty:
        print("❌ No data scraped.")
        return

    os.makedirs("data", exist_ok=True)
    out_path = "data/competitor_prices.csv"
    df.to_csv(out_path, index=False)
    print(f"\n✅ Done! {len(df)} books saved to {out_path}")
    print(df.describe())

if __name__ == "__main__":
    main()
