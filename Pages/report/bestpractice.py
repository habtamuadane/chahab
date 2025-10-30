import streamlit as st
import pandas as pd
import sqlite3
from datetime import date

class BestPractice:
    DB_FILE = "bestpractice_data.db"

    def __init__(self):
        # Ensure table exists
        with sqlite3.connect(self.DB_FILE) as conn:
            c = conn.cursor()
            c.execute("""
                CREATE TABLE IF NOT EXISTS exports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item TEXT,
                    industry TEXT,
                    country TEXT,
                    quantity REAL,
                    value_usd REAL,
                    export_date TEXT
                )
            """)
            conn.commit()

    def add_record(self, item, industry, country, quantity, value_usd, export_date):
        with sqlite3.connect(self.DB_FILE) as conn:
            c = conn.cursor()
            c.execute("""
                INSERT INTO exports (item, industry, country, quantity, value_usd, export_date)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (item, industry, country, quantity, value_usd, export_date))
            conn.commit()

    def get_records(self):
        with sqlite3.connect(self.DB_FILE) as conn:
            df = pd.read_sql("SELECT * FROM exports", conn)
        return df

    def show(self):
        st.title("🌍 Best Practice Report ")

        st.subheader("➕ Add New Best Practice Record")
        with st.form("practice_form", clear_on_submit=True):
            export_item = st.text_input("Exported Item Name")
            industry = st.text_input("Exporting Industry Name")
            destination_country = st.text_input("Destination Country")
            quantity = st.number_input("Quantity (in tons)", min_value=0.0, step=0.1)
            value_usd = st.number_input("Export Value (in USD)", min_value=0.0, step=100.0)
            export_date = st.date_input("Date of Export", value=date.today())
            submit = st.form_submit_button("Save Export Record")

        if submit:
            self.add_record(
                export_item,
                industry,
                destination_country,
                quantity,
                value_usd,
                export_date.strftime("%Y-%m-%d")
            )
            st.success(f"✅ Export record for {export_item} saved successfully!")

        st.divider()
        st.subheader("📦 Best Practice Records Summary")

        df = self.get_records()
        if not df.empty:
            st.dataframe(df.drop(columns=["id"]))
            total_value = df["value_usd"].sum()
            total_quantity = df["quantity"].sum()
            st.metric("🌍 Total Export Value (USD)", f"${total_value:,.2f}")
            st.metric("📦 Total Quantity (tons)", f"{total_quantity:,.2f}")
        else:
            st.info("No export records yet. Add one using the form above.")

# Run the app
if __name__ == "__main__":
    export_app = BestPractice()
    export_app.show()
