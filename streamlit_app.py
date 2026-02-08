import streamlit as st
from st_gsheets_connection import GSheetsConnection

# 1. SECURE CONFIG
FARM_NAME = "Jayeone Farms"
SECRET_KEY = st.secrets["SECRET_KEY"]

st.set_page_config(page_title=FARM_NAME, page_icon="🌱")

# 2. THE CONNECTION
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_cat = conn.read(worksheet="CATALOGUE")
    st.success("Digital Fortress Live!")
except Exception as e:
    st.error(f"Secret Handshake Failed: {e}")
    st.info("Check your triple-quotes (''') in the Secrets tab.")
    df_cat = None

# 3. UI
st.title(f"🌱 {FARM_NAME} OS")
if df_cat is not None:
    st.dataframe(df_cat)
