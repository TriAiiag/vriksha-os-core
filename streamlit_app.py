import streamlit as st
import pandas as pd

# --- 1. SETUP ---
FARM_NAME = "Jayeone Farms"
st.set_page_config(page_title=FARM_NAME, page_icon="🌱", layout="wide")

# --- 2. DATA FETCHING ---
def get_clean_url(raw_url, gid):
    # This ensures no hidden spaces or /edit junk breaks the link
    base = raw_url.split('/edit')[0].strip()
    return f"{base}/export?format=csv&gid={gid}"

try:
    # Pulling from your private Secrets
    raw_spreadsheet_url = st.secrets["spreadsheet_url"]
    
    @st.cache_data(ttl=60)
    def fetch_data(gid):
        final_url = get_clean_url(raw_spreadsheet_url, gid)
        return pd.read_csv(final_url)

    # --- 3. NAVIGATION ---
    st.sidebar.title("🚜 Farm Manager")
    page = st.sidebar.radio("View Dashboard:", ["Orders", "Catalogue", "Stock"])

    st.title(f"🌱 {FARM_NAME} OS")

    if page == "Orders":
        st.subheader("📦 Real-Time Orders")
        df = fetch_data("0")
        # Updated for 2026 Streamlit standards
        st.dataframe(df, width="stretch")

    elif page == "Catalogue":
        st.subheader("🥗 Product Catalogue")
        df = fetch_data("1277793309") 
        st.dataframe(df, width="stretch")

    elif page == "Stock":
        st.subheader("📉 Inventory Status")
        # Using the GID for your STOCK tab
        df = fetch_data("1374567283") 
        st.dataframe(df, width="stretch")

except Exception as e:
    st.error(f"Handshake Error: {e}")
    st.info("Check that 'spreadsheet_url' in Secrets is a single, clean line.")
