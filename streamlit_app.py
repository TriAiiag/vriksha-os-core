import streamlit as st
import pandas as pd

# --- 1. SETUP ---
FARM_NAME = "Jayeone Farms"
st.set_page_config(page_title=FARM_NAME, page_icon="🌱", layout="wide")

# --- 2. DATA FETCHING ---
# We use the 'pub' (Publish to Web) format which is more stable than the '/export' format
@st.cache_data(ttl=60)
def fetch_data(sid, gid):
    # This is a different URL structure that bypasses the 400 Bad Request bug
    url = f"https://docs.google.com/spreadsheets/d/{sid}/gviz/tq?tqx=out:csv&gid={gid}"
    return pd.read_csv(url)

try:
    sid = st.secrets["SHEET_ID"].strip()
    
    st.sidebar.title("🚜 Farm Manager")
    page = st.sidebar.radio("View:", ["Orders", "Catalogue", "Stock"])

    st.title(f"🌱 {FARM_NAME} OS")

    if page == "Orders":
        st.dataframe(fetch_data(sid, "0"), width="stretch")
    elif page == "Catalogue":
        st.dataframe(fetch_data(sid, "1277793309"), width="stretch")
    elif page == "Stock":
        st.dataframe(fetch_data(sid, "1374567283"), width="stretch")

except Exception as e:
    st.error(f"Handshake Error: {e}")
    st.info("Check: Google Sheet > File > Share > Publish to web (Entire Document as CSV).")
