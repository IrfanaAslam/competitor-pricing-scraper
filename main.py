from scrapers.competitor1 import scrape_competitor1
from scrapers.competitor2 import scrape_competitor2
import pandas as pd

def main():
    data1 = scrape_competitor1()
    data2 = scrape_competitor2()

    all_data = data1 + data2
    df = pd.DataFrame(all_data)

    df.to_csv("data/competitor_prices.csv", index=False)
    print("✅ Data scraping completed successfully!")

if __name__ == "__main__":
    main()
