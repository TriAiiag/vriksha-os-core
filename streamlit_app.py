import streamlit as st
import pandas as pd

# 1. SETTINGS
FARM_NAME = "Jayeone Farms"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1mnWUg74jdlwDT2w7nd05N7hOhXuOj0TlCYAsfUOgLvc/export?format=csv&gid=0"

st.set_page_config(page_title=FARM_NAME, page_icon="🌱")

# 2. THE MANUAL HANDSHAKE
@st.cache_data(ttl=600)
def load_farm_data(url):
    try:
        # We bypass the complex library and read the CSV directly from Google
        return pd.read_csv(url)
    except Exception as e:
        st.error(f"Handshake Error: {e}")
        return None

df_cat = load_farm_data(SHEET_URL)

# 3. UI
st.title(f"🌱 {FARM_NAME} OS")

if df_cat is not None:
    st.success("Digital Fortress: ONLINE")
    st.dataframe(df_cat, use_container_width=True)
else:
    st.warning("Awaiting connection to Jayeone Farms...")
