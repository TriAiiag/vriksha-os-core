import streamlit as st
import pandas as pd

# --- 1. SETUP ---
FARM_NAME = "Jayeone Farms"
st.set_page_config(page_title=FARM_NAME, page_icon="🌱", layout="wide")

# --- 2. DATA FETCHING ---
try:
    # We pull ONLY the ID and build a fresh, clean link
    sheet_id = st.secrets["SHEET_ID"].strip()
    
    @st.cache_data(ttl=60)
    def fetch_data(gid_code):
        # This is the industry-standard clean export URL
        export_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid_code}"
        return pd.read_csv(export_url)

    # --- 3. NAVIGATION ---
    st.sidebar.title("🚜 Farm Manager")
    page = st.sidebar.radio("View Dashboard:", ["Orders", "Catalogue", "Stock"])

    st.title(f"🌱 {FARM_NAME} OS")

    if page == "Orders":
        st.subheader("📦 Real-Time Orders")
        df = fetch_data("0") 
        st.dataframe(df, width="stretch")

    elif page == "Catalogue":
        st.subheader("🥗 Product Catalogue")
        df = fetch_data("1277793309") 
        st.dataframe(df, width="stretch")

    elif page == "Stock":
        st.subheader("📉 Inventory Status")
        df = fetch_data("1374567283") 
        st.dataframe(df, width="stretch")

except Exception as e:
    st.error(f"Handshake Error: {e}")
    st.info("Ensure Secrets has SHEET_ID set to only the ID string (the text between /d/ and /edit).")
