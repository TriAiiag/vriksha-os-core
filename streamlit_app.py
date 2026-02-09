import streamlit as st
import pandas as pd
from gspread_pandas import Spread
from google.oauth2 import service_account

# --- CONFIG ---
SHEET_ID = "1mnWUg74jdlwDT2w7ndO5N7hOhXuOj0TICYAsfUOgLvc"

def load_data():
    try:
        # Connect with your shared service account
        creds = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        )
        spread = Spread(SHEET_ID, creds=creds)
        
        # Load sheets exactly as they are named now
        orders_df = spread.sheet_to_df(sheet="ORDERS", index=None)
        stock_df = spread.sheet_to_df(sheet="STOCK", index=None)
        catalog_df = spread.sheet_to_df(sheet="CATALOGUE", index=None)
        
        return orders_df, stock_df, catalog_df, spread
    except Exception as e:
        st.error(f"❌ Connection Error: {e}")
        return None, None, None, None

orders, stock, catalog, spread_obj = load_data()

if orders is not None:
    st.title("🌿 Jayeone Farms OS")
    
    # 1. LIVE REVENUE (Pulled from your auto-calculating Column J)
    rev = pd.to_numeric(orders['Total'], errors='coerce').sum()
    st.metric("Est. Revenue", f"₹{rev:,.2f}")

    # 2. THE ORDER MANAGER
    # This matches your new column structure exactly
    veggie_options = catalog['Item_Name'].tolist()
    
    edited_orders = st.data_editor(
        orders,
        column_config={
            "Item_Name": st.column_config.SelectboxColumn("Vegetable", options=veggie_options),
            "Qty_Ordered": st.column_config.NumberColumn("Quantity", min_value=0),
            "Total": st.column_config.NumberColumn("Amount", disabled=True), # Read-only
            "Packed?": st.column_config.CheckboxColumn("Packed")
        },
        hide_index=True,
        width="stretch"
    )

    if st.button("🔄 Sync Orders & Stock"):
        spread_obj.df_to_sheet(edited_orders, sheet="ORDERS", index=False, replace=True)
        st.success("Successfully synced to TriAiiag Cloud!")
