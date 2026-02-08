import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# --- 1. SETUP ---
st.set_page_config(page_title="Jayeone Farms OS", page_icon="🌱", layout="wide")

# --- 2. THE ENGINE ---
def get_gspread_client():
    creds_dict = st.secrets["gspread_credentials"]
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    return gspread.authorize(creds)

@st.cache_data(ttl=60)
def fetch_data(sid, gid):
    url = f"https://docs.google.com/spreadsheets/d/{sid}/export?format=csv&gid={gid}"
    return pd.read_csv(url)

try:
    sid = st.secrets["SHEET_ID"].strip()
    page = st.sidebar.radio("Dashboard:", ["Orders", "Catalogue", "Stock"])

    if page == "Orders":
        st.subheader("📦 Incoming Orders")
        raw_df = fetch_data(sid, "0")
        
        # --- CLEANUP ---
        raw_df.columns = raw_df.columns.str.strip()
        display_df = raw_df.drop(columns=["Packed/Dispatched", "Status", "Timestamp"], errors='ignore')
        
        # Kill the 'None' rows from view
        display_df = display_df[display_df.iloc[:, 0].notna()].copy()

        # THE INTERACTIVE EDITOR
        edited_df = st.data_editor(display_df, width="stretch", hide_index=True)

        if st.button("💾 Save to Google Sheet"):
            with st.spinner("Writing to Digital Fortress..."):
                # --- THE FIX: Clean 'None' values before saving ---
                # This prevents the 'Out of range float' JSON error
                clean_df = edited_df.fillna("") 
                
                client = get_gspread_client()
                sh = client.open_by_key(sid)
                worksheet = sh.worksheet("ORDERS") 
                
                # Convert to list and update
                data_to_save = [clean_df.columns.values.tolist()] + clean_df.values.tolist()
                worksheet.update(data_to_save)
                
                st.success("✅ Records Successfully Updated!")
                st.cache_data.clear()

    elif page == "Catalogue":
        df = fetch_data(sid, "1608295230").dropna(how='all')
        st.dataframe(df, width="stretch", hide_index=True)

    elif page == "Stock":
        df = fetch_data(sid, "1277793309").dropna(how='all')
        st.dataframe(df, width="stretch", hide_index=True)

except Exception as e:
    st.error(f"⚠️ {e}")
