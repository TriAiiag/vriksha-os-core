import streamlit as st
import pandas as pd

# --- 1. SETUP ---
FARM_NAME = "Jayeone Farms"
st.set_page_config(page_title=FARM_NAME, page_icon="🌱", layout="wide")

# --- 2. THE ENGINE ---
def get_export_url(sid, gid):
    return f"https://docs.google.com/spreadsheets/d/{sid}/export?format=csv&gid={gid}"

try:
    # Uses the clean SHEET_ID from your private Secrets
    sid = st.secrets["SHEET_ID"].strip()
    
    @st.cache_data(ttl=60)
    def fetch_data(gid):
        url = get_export_url(sid, gid)
        return pd.read_csv(url)

    # --- 3. NAVIGATION SIDEBAR ---
    st.sidebar.title("🚜 Farm Manager")
    page = st.sidebar.radio("View Dashboard:", ["Orders", "Catalogue", "Stock Status"])

    st.title(f"🌱 {FARM_NAME} OS")

    if page == "Orders":
        st.subheader("📦 Incoming Orders")
        # GID 0 is the 'ORDERS' tab
        st.dataframe(fetch_data("0"), width="stretch")

    elif page == "Catalogue":
        st.subheader("🥗 Product List & Pricing")
        # Updated GID from your screenshot for 'CATALOGUE'
        st.dataframe(fetch_data("1608295230"), width="stretch")

    elif page == "Stock Status":
        st.subheader("📉 Inventory Levels")
        # Updated GID from your screenshot for 'STOCK'
        st.dataframe(fetch_data("1277793309"), width="stretch")

except Exception as e:
    st.error(f"System Error: {e}")
    st.info("Ensure your SHEET_ID in Streamlit Secrets is only the ID string.")
