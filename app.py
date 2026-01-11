import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.express as px

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Competitor Pricing Scraper",
    layout="wide",
    page_icon="💰"
)

# ---------- PAGE TITLE ----------
st.title("💰 Competitor Pricing Scraper Dashboard")
st.markdown("""
Scrape product prices from a default e-commerce site or your own link.
Visualize pricing insights and showcase your data skills.
""")

# ---------- TABS ----------
tab1, tab2 = st.tabs(["Default Scraper", "Custom URL Scraper"])

# ---------- FUNCTION TO SCRAPE BOOKS TO SCRAPE ----------
def scrape_books(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        products = []
        for item in soup.select('article.product_pod'):
            name = item.h3.a['title']
            price_text = item.select_one('p.price_color').text
            price = float(price_text.replace("£", "").replace("Â", ""))
            products.append({"Name": name, "Price": price})

        df = pd.DataFrame(products)
        return df
    except Exception as e:
        st.error(f"Error scraping: {e}")
        return pd.DataFrame()

# ---------- DEFAULT SCRAPER TAB ----------
with tab1:
    st.header("📚 Default Scraper (Books to Scrape)")
    default_url = "https://books.toscrape.com/"
    df_default = scrape_books(default_url)

    if not df_default.empty:
        # Stats Cards
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Products Found", len(df_default))
        col2.metric("Average Price", f"£{df_default['Price'].mean():.2f}")
        col3.metric("Minimum Price", f"£{df_default['Price'].min():.2f}")
        col4.metric("Maximum Price", f"£{df_default['Price'].max():.2f}")

        # Filter by Price
        min_price, max_price = st.slider(
            "Filter by Price Range (£)",
            min_value=float(df_default['Price'].min()),
            max_value=float(df_default['Price'].max()),
            value=(float(df_default['Price'].min()), float(df_default['Price'].max()))
        )
        filtered_df = df_default[(df_default['Price'] >= min_price) & (df_default['Price'] <= max_price)]

        # Table
        st.subheader("📋 Products Table")
        st.dataframe(filtered_df)

        # Plot
        st.subheader("📊 Price Distribution")
        fig = px.bar(filtered_df, x='Name', y='Price', text='Price',
                     labels={'Price': 'Price (£)'}, hover_data=['Name'])
        fig.update_layout(height=500, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data found for the default scraper.")

# ---------- USER INPUT SCRAPER TAB ----------
with tab2:
    st.header("🌐 Custom URL Scraper")
    user_url = st.text_input("Enter any product page URL:")

    if user_url:
        df_user = scrape_books(user_url)
        if not df_user.empty:
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Products Found", len(df_user))
            col2.metric("Average Price", f"£{df_user['Price'].mean():.2f}")
            col3.metric("Minimum Price", f"£{df_user['Price'].min():.2f}")
            col4.metric("Maximum Price", f"£{df_user['Price'].max():.2f}")

            min_price, max_price = st.slider(
                "Filter by Price Range (£)",
                min_value=float(df_user['Price'].min()),
                max_value=float(df_user['Price'].max()),
                value=(float(df_user['Price'].min()), float(df_user['Price'].max()))
            )
            filtered_df = df_user[(df_user['Price'] >= min_price) & (df_user['Price'] <= max_price)]

            st.subheader("📋 Products Table")
            st.dataframe(filtered_df)

            st.subheader("📊 Price Distribution")
            fig = px.bar(filtered_df, x='Name', y='Price', text='Price',
                         labels={'Price': 'Price (£)'}, hover_data=['Name'])
            fig.update_layout(height=500, xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No products found or page structure not compatible.")

# ---------- FOOTER ----------
st.markdown("""
---
Made with ❤️ by **Irfana Aslam** | Showcase your scraping & visualization skills!
""")
