def clean_price(price_text):
    return price_text.replace("$", "").replace(",", "").strip()

def normalize_stock(stock_text):
    stock_text = stock_text.lower()
    if "out" in stock_text:
        return "Out of Stock"
    return "In Stock"
