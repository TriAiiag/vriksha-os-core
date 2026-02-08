import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# --- 1. CONFIG ---
FARM_NAME = "Jayeone Farms OS"
st.set_page_config(page_title=FARM_NAME, page_icon="🌱", layout="wide")

# --- 2. THE ENGINE ---
def get_gspread_client():
    creds_dict = st.secrets["gspread_credentials"]
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    return gspread.authorize(creds)

@st.cache_data(ttl=300)
def fetch_data(sid, gid):
    url = f"https://docs.google.com/spreadsheets/d/{sid}/export?format=csv&gid={gid}"
    return pd.read_csv(url)

try:
    sid = st.secrets["SHEET_ID"].strip()
    st.sidebar.title("🚜 Jayeone Navigation")
    page = st.sidebar.radio("Go to:", ["Orders Dashboard", "Catalogue", "Inventory"])

    if page == "Orders Dashboard":
        raw_df = fetch_data(sid, "0")
        raw_df.columns = raw_df.columns.str.strip()
        df = raw_df[raw_df.iloc[:, 0].notna()].copy()

        # --- FEATURE 1: THE MORNING BRIEFING (Intelligence) ---
        total_orders = len(df)
        # Assuming 'Total_Price' or 'Amount' column exists; adjust name as needed
        revenue_col = next((c for c in df.columns if 'Price' in c or 'Amount' in c), None)
        total_revenue = df[revenue_col].sum() if revenue_col else 0
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Orders", f"{total_orders}")
        col2.metric("Est. Revenue", f"₹{total_revenue:,.2f}")
        col3.metric("Status", "Operational")

        st.divider()

        # --- FEATURE 2: ROUTE INTELLIGENCE (Filtering) ---
        # Assuming 'City' or 'Location' column exists
        city_col = next((c for c in df.columns if 'City' in c or 'Location' in c), None)
        if city_col:
            cities = ["All Locations"] + sorted(df[city_col].unique().tolist())
            selected_city = st.selectbox("Filter by Delivery Route:", cities)
            if selected_city != "All Locations":
                df = df[df[city_col] == selected_city]

        # --- FEATURE 3: MOBILE TICK-MARKS ---
        if 'Packed/Dispatched' in df.columns:
            df['Packed/Dispatched'] = df['Packed/Dispatched'].apply(
                lambda x: True if str(x).upper() == "TRUE" else False
            )

        # Drop technical clutter
        display_df = df.drop(columns=["Status", "Timestamp"], errors='ignore')

        edited_df = st.data_editor(
            display_df,
            column_config={
                "Packed/Dispatched": st.column_config.CheckboxColumn("Packed?", default=False)
            },
            disabled=[col for col in display_df.columns if col != "Packed/Dispatched"],
            width="stretch",
            hide_index=True
        )

        if st.button("💾 Sync Packing Progress"):
            with st.spinner("Updating Digital Fortress..."):
                client = get_gspread_client()
                sh = client.open_by_key(sid)
                worksheet = sh.worksheet("ORDERS")
                # Clean NaNs for JSON compliance before writing
                clean_df = edited_df.fillna("")
                data_to_save = [clean_df.columns.values.tolist()] + clean_df.values.tolist()
                worksheet.update(data_to_save)
                st.success("✅ Records Synced!")
                st.cache_data.clear()

    # (Catalogue and Inventory tabs remain as simple dataframes for now)
    elif page == "Catalogue":
        st.dataframe(fetch_data(sid, "1608295230").dropna(how='all'), use_container_width=True, hide_index=True)

    elif page == "Inventory":
        st.dataframe(fetch_data(sid, "1277793309").dropna(how='all'), use_container_width=True, hide_index=True)

except Exception as e:
    st.error(f"System Error: {e}")
