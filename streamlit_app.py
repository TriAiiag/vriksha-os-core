import streamlit as st
import pandas as pd

# --- 1. SETUP & THEME ---
FARM_NAME = "Jayeone Farms"
st.set_page_config(page_title=FARM_NAME, page_icon="🌱", layout="wide")

# Custom CSS to fix the Red color conflict and make it clean
st.markdown("""
    <style>
    .stCheckbox { color: #2E7D32; } /* Changes checkbox text to Farm Green */
    .stDataFrame { border: 1px solid #e6e9ef; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE ENGINE ---
@st.cache_data(ttl=600)
def fetch_data(sid, gid):
    url = f"https://docs.google.com/spreadsheets/d/{sid}/export?format=csv&gid={gid}"
    df = pd.read_csv(url)
    df = df.dropna(how='all').reset_index(drop=True)
    df = df[df.iloc[:, 0].notna()]
    return df

try:
    sid = st.secrets["SHEET_ID"].strip()
    
    st.sidebar.title("🚜 Farm Manager")
    page = st.sidebar.radio("View Dashboard:", ["Orders", "Catalogue", "Stock Status"])
    
    if st.sidebar.button("🔄 Sync New Data"):
        st.cache_data.clear()
        st.rerun()

    st.title(f"🌱 {FARM_NAME} OS")

    if page == "Orders":
        st.subheader("📦 Incoming Orders")
        df = fetch_data(sid, "0")
        
        # ADDING INTERACTIVITY: The "Selection" checkbox
        # This replaces the messy red highlight with a clean selection tool
        edited_df = st.data_editor(
            df,
            column_config={
                "Status": st.column_config.CheckboxColumn(
                    "Pack Status",
                    help="Check once item is packed",
                    default=False,
                )
            },
            disabled=["Order_ID", "Date", "Customer_Name", "Items"], # Stops accidental editing
            width="stretch"
        )

    elif page == "Catalogue":
        st.subheader("🥗 Product List & Pricing")
        df = fetch_data(sid, "1608295230")
        st.dataframe(df, width="stretch")

    elif page == "Stock Status":
        st.subheader("📉 Inventory Status")
        df = fetch_data(sid, "1277793309")
        st.dataframe(df, width="stretch")

except Exception as e:
    st.error(f"System Error: {e}")
