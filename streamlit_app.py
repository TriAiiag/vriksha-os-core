import streamlit as st
import pandas as pd

# 1. PRIVATE CONFIG
FARM_NAME = "Jayeone Farms"
st.set_page_config(page_title=FARM_NAME, page_icon="🌱", layout="wide")

# This pulls the URL from your PRIVATE Secrets tab instead of the code
# Make sure your Secrets has: spreadsheet_url = "https://docs.google.com/..."
BASE_URL = st.secrets["spreadsheet_url"].split('/edit')[0]

# 2. NAVIGATION SIDEBAR
st.sidebar.title("🚜 Navigation")
page = st.sidebar.radio("Go to:", ["Orders", "Catalogue", "Stock"])

@st.cache_data(ttl=60)
def get_data(gid):
    url = f"{BASE_URL}/export?format=csv&gid={gid}"
    return pd.read_csv(url)

# 3. PAGE LOGIC (Using your actual Sheet GIDs)
st.title(f"🌱 {FARM_NAME} OS")

if page == "Orders":
    st.subheader("📦 Recent Orders")
    df = get_data("0") # GID for Orders
    st.dataframe(df, use_container_width=True)

elif page == "Catalogue":
    st.subheader("🥗 Price List")
    df = get_data("1277793309") # GID from your screenshot for Catalogue
    st.dataframe(df, use_container_width=True)

elif page == "Stock":
    st.subheader("📉 Inventory Levels")
    df = get_data("123456789") # Replace with your actual STOCK GID
    st.dataframe(df, use_container_width=True)
