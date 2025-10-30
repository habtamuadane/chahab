import streamlit as st
import pandas as pd
from datetime import date

class Extension:
    def __init__(self):
        # Store export data in session
        if "export_data" not in st.session_state:
            st.session_state["export_data"] = []

    def show(self):
        st.title("🌍 Export Report – Foreign Trade")

        st.subheader("➕ Add New Export Record")
        with st.form("export_form", clear_on_submit=True):
            export_item = st.text_input("Exported Item Name")
            industry = st.text_input("Exporting Industry Name")
            destination_country = st.text_input("Destination Country")
            quantity = st.number_input("Quantity (in tons)", min_value=0.0, step=0.1)
            value_usd = st.number_input("Export Value (in USD)", min_value=0.0, step=100.0)
            export_date = st.date_input("Date of Export", value=date.today())
            submit = st.form_submit_button("Save Export Record")

        if submit:
            st.session_state["export_data"].append({
                "Item": export_item,
                "Industry": industry,
                "Country": destination_country,
                "Quantity (tons)": quantity,
                "Value (USD)": value_usd,
                "Date": export_date.strftime("%Y-%m-%d")
            })
            st.success(f"✅ Export record for {export_item} saved successfully!")

        st.divider()
        st.subheader("📦 Export Records Summary")

        if st.session_state["export_data"]:
            df = pd.DataFrame(st.session_state["export_data"])
            st.dataframe(df)

            total_value = df["Value (USD)"].sum()
            total_quantity = df["Quantity (tons)"].sum()
            st.metric("🌍 Total Export Value (USD)", f"${total_value:,.2f}")
            st.metric("📦 Total Quantity (tons)", f"{total_quantity:,.2f}")

        else:
            st.info("No export records yet. Add one using the form above.")
