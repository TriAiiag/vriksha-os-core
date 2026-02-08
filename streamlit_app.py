import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# --- 1. SETUP ---
FARM_NAME = "Jayeone Farms"
st.set_page_config(page_title=FARM_NAME, page_icon="🌱", layout="wide")

# --- 2. THE DATA ENGINES ---
def get_gspread_client():
    creds_dict = st.secrets["gspread_credentials"]
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    return gspread.authorize(creds)

@st.cache_data(ttl=60) # Refreshes every minute for better sync
def fetch_data(sid, gid):
    url = f"https://docs.google.com/spreadsheets/d/{sid}/export?format=csv&gid={gid}"
    return pd.read_csv(url).dropna(how='all')

try:
    sid = st.secrets["SHEET_ID"].strip()
    
    st.sidebar.title("🚜 Farm Manager")
    page = st.sidebar.radio("View Dashboard:", ["Orders", "Catalogue", "Stock Status"])

    if st.sidebar.button("🔄 Force Refresh"):
        st.cache_data.clear()
        st.rerun()

    st.title(f"🌱 {FARM_NAME} OS")

    if page == "Orders":
        st.subheader("📦 Incoming Orders")
        raw_df = fetch_data(sid, "0")
        
        # --- THE CLEANUP: Explicitly remove the ghost columns ---
        # This solves the "Still visible" problem
        cols_to_hide = ["Packed/Dispatched", "Status", "packed/dispatched"]
        display_df = raw_df.drop(columns=[c for c in cols_to_hide if c in raw_df.columns], errors='ignore')
        
        # Ensure the table is interactive
        edited_df = st.data_editor(display_df, width="stretch", hide_index=True, key="main_editor")

        if st.button("💾 Save All Changes"):
            with st.spinner("Writing to Digital Fortress..."):
                client = get_gspread_client()
                # Instead of 'sheet1', we open the specific spreadsheet and the first tab
                sh = client.open_by_key(sid)
                worksheet = sh.get_worksheet(0) # '0' is the Orders tab
                
                # Convert the edited dataframe back to a list for Google
                updated_values = [edited_df.columns.values.tolist()] + edited_df.values.tolist()
                worksheet.update(updated_values)
                
                st.success("✅ Google Sheet Updated!")
                st.cache_data.clear() # Clears cache so you see the new data immediately

    elif page == "Catalogue":
        st.dataframe(fetch_data(sid, "1608295230"), width="stretch", hide_index=True)

    elif page == "Stock Status":
        st.dataframe(fetch_data(sid, "1277793309"), width="stretch", hide_index=True)

except Exception as e:
    st.error(f"System Error: {e}")
