"""
app.py — Competitor Pricing Scraper Dashboard v2
Run with:  python -m streamlit run app.py
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

from scraper import scrape_books, scrape_custom_url, scrape_category, CATEGORIES

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Pricing Intelligence Dashboard",
    layout="wide",
    page_icon="",
    initial_sidebar_state="expanded",
)

# ── Theme toggle ──────────────────────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = True

# ── CSS ───────────────────────────────────────────────────────────────────────
dark = st.session_state["dark_mode"]

BG       = "#0f1117" if dark else "#f5f7fa"
CARD     = "#1a1d27" if dark else "#ffffff"
ACCENT   = "#00d4aa"
ACCENT2  = "#ff6b6b"
TEXT     = "#6f8eec" if dark else "#1a1d27"
SUBTEXT  = "#8b8fa8" if dark else "#6b7280"
BORDER   = "#2a2d3e" if dark else "#e2e8f0"
PLOT_BG  = "#1a1d27" if dark else "#ffffff"
PAPER_BG = "#0f1117" if dark else "#f5f7fa"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {{
    font-family: 'Syne', sans-serif;
    background-color: {BG};
    color: {TEXT};
}}
.block-container {{ padding: 1.5rem 2rem 2rem 2rem; max-width: 1400px; }}
.stTabs [data-baseweb="tab-list"] {{
    background: {CARD};
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
    border: 1px solid {BORDER};
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 8px;
    color: {SUBTEXT};
    font-weight: 600;
    font-size: 0.85rem;
    padding: 8px 18px;
}}
.stTabs [aria-selected="true"] {{
    background: {ACCENT} !important;
    color: #0f1117 !important;
}}
.metric-box {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 20px 24px;
    text-align: center;
    transition: transform 0.2s;
}}
.metric-box:hover {{ transform: translateY(-2px); }}
.metric-label {{
    font-size: 0.75rem;
    font-weight: 600;
    color: {SUBTEXT};
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 6px;
}}
.metric-value {{
    font-size: 1.9rem;
    font-weight: 800;
    color: {ACCENT};
    font-family: 'DM Mono', monospace;
    line-height: 1;
}}
.metric-sub {{
    font-size: 0.72rem;
    color: {SUBTEXT};
    margin-top: 4px;
}}
.section-header {{
    font-size: 1.1rem;
    font-weight: 700;
    color: {TEXT};
    margin: 1.5rem 0 0.8rem 0;
    display: flex;
    align-items: center;
    gap: 8px;
}}
.insight-card {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-left: 3px solid {ACCENT};
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 10px;
    font-size: 0.88rem;
    color: {TEXT};
}}
.badge {{
    display: inline-block;
    background: {ACCENT}22;
    color: {ACCENT};
    border: 1px solid {ACCENT}44;
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.72rem;
    font-weight: 600;
    margin-left: 8px;
}}
.stButton > button {{
    background: {ACCENT};
    color: #0f1117;
    font-weight: 700;
    border: none;
    border-radius: 8px;
    padding: 10px 24px;
    font-family: 'Syne', sans-serif;
    transition: opacity 0.2s;
}}
.stButton > button:hover {{ opacity: 0.85; }}
div[data-testid="stMetric"] {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 16px;
}}
.stDataFrame {{ border-radius: 12px; overflow: hidden; }}
.stSelectbox > div, .stMultiSelect > div, .stSlider > div {{
    background: {CARD};
}}
hr {{ border-color: {BORDER}; margin: 1.5rem 0; }}
</style>
""", unsafe_allow_html=True)

# ── Plotly theme helper ───────────────────────────────────────────────────────
def apply_theme(fig, height=420):
    fig.update_layout(
        height=height,
        plot_bgcolor=PLOT_BG,
        paper_bgcolor=PAPER_BG,
        font=dict(family="Syne, sans-serif", color=TEXT),
        xaxis=dict(gridcolor=BORDER, linecolor=BORDER),
        yaxis=dict(gridcolor=BORDER, linecolor=BORDER),
        margin=dict(l=20, r=20, t=40, b=20),
    )
    return fig

# ── Excel export helper ───────────────────────────────────────────────────────
def to_excel(df: pd.DataFrame) -> bytes:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Books")
    return output.getvalue()

# ── Metric cards ──────────────────────────────────────────────────────────────
def show_metrics(df: pd.DataFrame):
    cols = st.columns(5)
    stats = [
        ("📦 Total Books",    str(len(df)),                              "scraped"),
        ("💰 Avg Price",      f"£{df['Price (£)'].mean():.2f}",          "per book"),
        ("⬇️ Min Price",      f"£{df['Price (£)'].min():.2f}",           "cheapest"),
        ("⬆️ Max Price",      f"£{df['Price (£)'].max():.2f}",           "priciest"),
        ("⭐ Avg Rating",     f"{df['Rating (Stars)'].mean():.1f} / 5",  "stars"),
    ]
    for col, (label, value, sub) in zip(cols, stats):
        col.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

# ── Sidebar filters ───────────────────────────────────────────────────────────
def sidebar_filters(df: pd.DataFrame, prefix: str) -> pd.DataFrame:
    st.sidebar.markdown(f"### 🎛️ Filters")

    # Search
    search = st.sidebar.text_input("🔍 Search by title", key=f"{prefix}_search", placeholder="e.g. Great, Dark...")
    if search:
        df = df[df["Title"].str.contains(search, case=False, na=False)]

    # Price range
    lo, hi = float(df["Price (£)"].min()), float(df["Price (£)"].max())
    if lo < hi:
        price_range = st.sidebar.slider("💷 Price Range (£)", lo, hi, (lo, hi), key=f"{prefix}_price")
        df = df[(df["Price (£)"] >= price_range[0]) & (df["Price (£)"] <= price_range[1])]

    # Rating filter
    if "Rating (Stars)" in df.columns:
        min_rating = st.sidebar.select_slider(
            "⭐ Min Rating", options=[1, 2, 3, 4, 5], value=1, key=f"{prefix}_rating"
        )
        df = df[df["Rating (Stars)"] >= min_rating]

    # Availability filter
    if "Availability" in df.columns:
        avail_opts = df["Availability"].unique().tolist()
        selected_avail = st.sidebar.multiselect(
            "📦 Availability", avail_opts, default=avail_opts, key=f"{prefix}_avail"
        )
        df = df[df["Availability"].isin(selected_avail)] if selected_avail else df

    # Sort
    sort_col = st.sidebar.selectbox(
        "↕️ Sort by",
        ["Price (£)", "Rating (Stars)", "Value Score", "Title"],
        key=f"{prefix}_sort"
    )
    sort_asc = st.sidebar.radio("Order", ["Ascending", "Descending"], key=f"{prefix}_order") == "Ascending"
    df = df.sort_values(sort_col, ascending=sort_asc).reset_index(drop=True)

    st.sidebar.markdown(f"**{len(df)} books** match your filters")
    return df

# ── Products table ────────────────────────────────────────────────────────────
def show_table(df: pd.DataFrame, key_prefix: str = "default"):
    st.markdown('<div class="section-header">📋 Products Table</div>', unsafe_allow_html=True)
    display_df = df.copy()
    if "Rating (Stars)" in display_df.columns:
        display_df["Rating (Stars)"] = display_df["Rating (Stars)"].apply(lambda r: "⭐" * int(r))
    st.dataframe(display_df, width="stretch", height=380)

    c1, c2 = st.columns(2)
    with c1:
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download CSV", data=csv,
                           file_name="books_data.csv", mime="text/csv",
                           key=f"csv_{key_prefix}")
    with c2:
        try:
            excel_data = to_excel(df)
            st.download_button("📊 Download Excel", data=excel_data,
                               file_name="books_data.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                               key=f"excel_{key_prefix}")
        except Exception:
            st.info("Install `openpyxl` for Excel export: `pip install openpyxl`")

# ── Charts ────────────────────────────────────────────────────────────────────
def show_charts(df: pd.DataFrame, prefix: str = "default"):
    if df.empty:
        st.warning("No data to display after filtering.")
        return

    # Row 1: Bar + Histogram
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-header">📊 Top 25 by Price</div>', unsafe_allow_html=True)
        top = df.nlargest(25, "Price (£)")
        fig = px.bar(top, x="Title", y="Price (£)", color="Price (£)",
                     color_continuous_scale=[[0, "#2d6a9f"], [1, ACCENT]],
                     text="Price (£)")
        fig.update_traces(texttemplate="£%{text:.2f}", textposition="outside")
        fig.update_layout(xaxis_tickangle=-45, coloraxis_showscale=False, showlegend=False)
        st.plotly_chart(apply_theme(fig), width="stretch")

    with c2:
        st.markdown('<div class="section-header">📈 Price Distribution</div>', unsafe_allow_html=True)
        fig2 = px.histogram(df, x="Price (£)", nbins=25,
                            color_discrete_sequence=[ACCENT])
        fig2.update_layout(bargap=0.05)
        st.plotly_chart(apply_theme(fig2), width="stretch")

    # Row 2: Rating breakdown + Price buckets
    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="section-header">⭐ Avg Price by Rating</div>', unsafe_allow_html=True)
        avg = (df.groupby("Rating (Stars)")["Price (£)"]
                 .mean().reset_index()
                 .rename(columns={"Price (£)": "Avg Price (£)"}))
        fig3 = px.bar(avg, x="Rating (Stars)", y="Avg Price (£)",
                      color="Avg Price (£)",
                      color_continuous_scale=[[0, "#ff6b6b"], [1, ACCENT]],
                      text="Avg Price (£)")
        fig3.update_traces(texttemplate="£%{text:.2f}", textposition="outside")
        fig3.update_layout(coloraxis_showscale=False)
        st.plotly_chart(apply_theme(fig3, 380), width="stretch")

    with c4:
        st.markdown('<div class="section-header">🪣 Price Bucket Segments</div>', unsafe_allow_html=True)
        bins   = [0, 10, 20, 30, 40, 60]
        labels = ["£0–10", "£10–20", "£20–30", "£30–40", "£40–60"]
        df2 = df.copy()
        df2["Bucket"] = pd.cut(df2["Price (£)"], bins=bins, labels=labels, right=False)
        bucket_counts = df2["Bucket"].value_counts().sort_index().reset_index()
        bucket_counts.columns = ["Price Range", "Count"]
        fig4 = px.pie(bucket_counts, names="Price Range", values="Count",
                      color_discrete_sequence=[ACCENT, "#ff6b6b", "#f7c948", "#6bc5f8", "#b088f9"],
                      hole=0.45)
        fig4.update_traces(textinfo="percent+label", pull=[0.03]*len(bucket_counts))
        fig4.update_layout(showlegend=False)
        st.plotly_chart(apply_theme(fig4, 380), width="stretch")

    # Row 3: Rating distribution pie + scatter value map
    c5, c6 = st.columns(2)
    with c5:
        st.markdown('<div class="section-header">🥧 Rating Distribution</div>', unsafe_allow_html=True)
        rating_counts = df["Rating (Stars)"].value_counts().sort_index().reset_index()
        rating_counts.columns = ["Stars", "Count"]
        rating_counts["Label"] = rating_counts["Stars"].apply(lambda x: "⭐" * x)
        fig5 = px.pie(rating_counts, names="Label", values="Count", hole=0.4,
                      color_discrete_sequence=[ACCENT, "#6bc5f8", "#f7c948", "#ff6b6b", "#b088f9"])
        fig5.update_traces(textinfo="percent+label", pull=[0.03]*len(rating_counts))
        fig5.update_layout(showlegend=False)
        st.plotly_chart(apply_theme(fig5, 380), width="stretch")

    with c6:
        st.markdown('<div class="section-header">💎 Price vs Rating Scatter</div>', unsafe_allow_html=True)
        fig6 = px.scatter(df, x="Price (£)", y="Rating (Stars)",
                          size="Value Score", color="Value Score",
                          hover_name="Title",
                          color_continuous_scale=[[0, "#ff6b6b"], [0.5, "#f7c948"], [1, ACCENT]],
                          size_max=25)
        fig6.update_layout(coloraxis_colorbar=dict(title="Value"))
        st.plotly_chart(apply_theme(fig6, 380), width="stretch")


# ── Analytics tab ─────────────────────────────────────────────────────────────
def show_analytics(df: pd.DataFrame, prefix: str = "default"):
    if df.empty:
        st.warning("No data available.")
        return

    st.markdown('<div class="section-header">🏆 Top 10 Best Value Books</div>', unsafe_allow_html=True)
    st.caption("Value Score = (Rating ÷ Price) × 10  — higher is better bang for your buck")
    top_value = df.nlargest(10, "Value Score")[["Title", "Price (£)", "Rating (Stars)", "Value Score"]]
    top_value["Rating (Stars)"] = top_value["Rating (Stars)"].apply(lambda r: "⭐" * int(r))
    top_value.index = range(1, len(top_value) + 1)
    st.dataframe(top_value, width="stretch")

    st.markdown('<div class="section-header">📉 Price Trend Across Pages</div>', unsafe_allow_html=True)
    st.caption("Average price per scraped page — shows if prices vary by page position")
    if "Page" in df.columns and df["Page"].nunique() > 1:
        trend = df.groupby("Page")["Price (£)"].mean().reset_index()
        fig = px.line(trend, x="Page", y="Price (£)", markers=True,
                      color_discrete_sequence=[ACCENT])
        fig.update_traces(line_width=2.5, marker_size=7)
        fig.update_layout(xaxis_title="Page Number", yaxis_title="Avg Price (£)")
        st.plotly_chart(apply_theme(fig, 350), width="stretch")
    else:
        st.info("Scrape 2+ pages to see the price trend.")

    st.markdown('<div class="section-header">💡 Auto Insights</div>', unsafe_allow_html=True)
    avg  = df["Price (£)"].mean()
    cheap = df[df["Price (£)"] < avg]
    expensive = df[df["Price (£)"] >= avg]
    top_rated = df[df["Rating (Stars)"] == 5]
    best_val  = df.nlargest(1, "Value Score").iloc[0]

    insights = [
        f"📌 <b>{len(cheap)}</b> books ({len(cheap)/len(df)*100:.0f}%) are priced <b>below average</b> (£{avg:.2f})",
        f"📌 <b>{len(top_rated)}</b> books have a perfect <b>5-star rating</b>",
        f"📌 The <b>best value book</b> is <i>\"{best_val['Title'][:50]}...\"</i> — £{best_val['Price (£)']:.2f} with {int(best_val['Rating (Stars)'])}★ (score: {best_val['Value Score']})",
        f"📌 The <b>most expensive</b> book costs <b>£{df['Price (£)'].max():.2f}</b>, the cheapest <b>£{df['Price (£)'].min():.2f}</b> — a spread of £{df['Price (£)'].max() - df['Price (£)'].min():.2f}",
        f"📌 <b>{len(expensive)}</b> books ({len(expensive)/len(df)*100:.0f}%) are priced <b>above average</b>",
    ]
    for insight in insights:
        st.markdown(f'<div class="insight-card">{insight}</div>', unsafe_allow_html=True)


# ── Header ────────────────────────────────────────────────────────────────────
col_title, col_toggle = st.columns([5, 1])
with col_title:
    st.markdown(f"""
    <h1 style='font-size:2rem; font-weight:800; color:{TEXT}; margin:0;'>
        💹 Pricing Intelligence Dashboard
        <span class='badge'>v2.0</span>
    </h1>
    <p style='color:{SUBTEXT}; margin:4px 0 16px 0; font-size:0.9rem;'>
        Scrape · Analyse · Export — live e-commerce pricing data
    </p>
    """, unsafe_allow_html=True)

with col_toggle:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🌙 Dark" if not dark else "☀️ Light", key="theme_toggle"):
        st.session_state["dark_mode"] = not dark
        st.rerun()

# ── Main tabs ─────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📚 Default Scraper",
    "🗂️ Category Scraper",
    "🌐 Custom URL",
    "ℹ️ How to Use",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — Default scraper
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.sidebar.markdown("## ⚙️ Scraper Settings")
    pages = st.sidebar.slider("Pages to scrape", 1, 20, 3, key="t1_pages")
    st.sidebar.caption("Each page = 20 books. 50 pages = all 1,000 books.")

    if st.button("🚀 Scrape Books", key="t1_btn"):
        with st.spinner(f"Scraping {pages} page(s) — please wait..."):
            df = scrape_books(num_pages=pages)
        if not df.empty:
            st.session_state["default_df"] = df
            st.success(f"✅ Scraped **{len(df)}** books across **{pages}** page(s)!")
        else:
            st.error("❌ No data found. Check your connection.")

    if "default_df" in st.session_state:
        raw_df = st.session_state["default_df"]
        filtered_df = sidebar_filters(raw_df, "t1")
        show_metrics(filtered_df)
        st.divider()

        sub1, sub2 = st.tabs(["📊 Charts & Table", "🔬 Analytics"])
        with sub1:
            show_table(filtered_df, key_prefix="t1")
            show_charts(filtered_df, prefix="t1")
        with sub2:
            show_analytics(filtered_df, prefix="t1")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — Category scraper
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown(f"<p style='color:{SUBTEXT};'>Browse and scrape any of the 29 categories on books.toscrape.com</p>", unsafe_allow_html=True)

    cat_name = st.selectbox("📂 Choose a Category", list(CATEGORIES.keys()), key="cat_select")
    cat_slug = CATEGORIES[cat_name]

    if st.button(f"🚀 Scrape '{cat_name}'", key="t2_btn"):
        with st.spinner(f"Scraping all books in **{cat_name}**..."):
            df_cat = scrape_category(cat_slug)
        if not df_cat.empty:
            st.session_state["cat_df"] = df_cat
            st.session_state["cat_name"] = cat_name
            st.success(f"✅ Found **{len(df_cat)}** books in **{cat_name}**!")
        else:
            st.error("❌ No data found for this category.")

    if "cat_df" in st.session_state:
        raw_cat = st.session_state["cat_df"]
        filtered_cat = sidebar_filters(raw_cat, "t2")
        show_metrics(filtered_cat)
        st.divider()

        sub3, sub4 = st.tabs(["📊 Charts & Table", "🔬 Analytics"])
        with sub3:
            show_table(filtered_cat, key_prefix="t2")
            show_charts(filtered_cat, prefix="t2")
        with sub4:
            show_analytics(filtered_cat, prefix="t2")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — Custom URL
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown(f"<p style='color:{SUBTEXT};'>Paste any books.toscrape.com listing URL — https:// is optional.</p>", unsafe_allow_html=True)

    user_url = st.text_input(
        "🔗 Product listing URL",
        placeholder="http://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
        key="custom_url_input",
    )

    if st.button("🔍 Scrape URL", key="t3_btn") and user_url:
        with st.spinner("Scraping URL..."):
            df_custom = scrape_custom_url(user_url)
        if not df_custom.empty:
            st.session_state["custom_df"] = df_custom
            st.success(f"✅ Found **{len(df_custom)}** products!")
        else:
            st.error("❌ No products found. Check the URL or page structure.")

    if "custom_df" in st.session_state:
        raw_custom = st.session_state["custom_df"]
        filtered_custom = sidebar_filters(raw_custom, "t3")
        show_metrics(filtered_custom)
        st.divider()

        sub5, sub6 = st.tabs(["📊 Charts & Table", "🔬 Analytics"])
        with sub5:
            show_table(filtered_custom, key_prefix="t3")
            show_charts(filtered_custom, prefix="t3")
        with sub6:
            show_analytics(filtered_custom, prefix="t3")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — How to Use
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown(f"""
    <div style='max-width:700px;'>

    <h3 style='color:{TEXT}'>🚀 Getting Started</h3>
    <div class='insight-card'>
    <b>1. Default Scraper</b> — Choose how many pages to scrape (1 page = 20 books) and click <b>Scrape Books</b>.
    </div>
    <div class='insight-card'>
    <b>2. Category Scraper</b> — Pick a genre from the dropdown (e.g. Mystery, Science Fiction) and scrape all books in that category.
    </div>
    <div class='insight-card'>
    <b>3. Custom URL</b> — Paste any books.toscrape.com listing URL. The https:// prefix is optional — we add it automatically.
    </div>

    <h3 style='color:{TEXT}; margin-top:1.5rem;'>🎛️ Filters (Sidebar)</h3>
    <div class='insight-card'>Use the sidebar to <b>search by title keyword</b>, filter by <b>price range</b>, set a <b>minimum star rating</b>, filter by <b>availability</b>, and <b>sort</b> by any column.</div>

    <h3 style='color:{TEXT}; margin-top:1.5rem;'>🔬 Analytics Tab</h3>
    <div class='insight-card'>Each scraper tab has a <b>Charts & Table</b> view and an <b>Analytics</b> view. Analytics shows the <b>Top 10 Best Value</b> books, a <b>Price Trend</b> across pages, and <b>Auto Insights</b>.</div>

    <h3 style='color:{TEXT}; margin-top:1.5rem;'>💡 Value Score</h3>
    <div class='insight-card'>Value Score = (Rating ÷ Price) × 10. A £5 book with 5 stars scores <b>10.0</b>. A £50 book with 5 stars scores <b>1.0</b>. Use this to find hidden gems.</div>

    <h3 style='color:{TEXT}; margin-top:1.5rem;'>📤 Export</h3>
    <div class='insight-card'>Download your filtered data as <b>CSV</b> or <b>Excel (.xlsx)</b> from the Products Table section.</div>

    <h3 style='color:{TEXT}; margin-top:1.5rem;'>🌙 Theme</h3>
    <div class='insight-card'>Toggle between <b>Dark</b> and <b>Light</b> mode using the button in the top-right corner.</div>

    </div>
    """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    f"<p style='text-align:center; color:{SUBTEXT}; font-size:0.8rem;'>"
    "Made with ❤️ by <b>Irfana Aslam</b> &nbsp;|&nbsp; "
    "Pricing Intelligence Dashboard v2.0 &nbsp;|&nbsp; "
    "Built with Streamlit · BeautifulSoup · Plotly"
    "</p>",
    unsafe_allow_html=True,
)
