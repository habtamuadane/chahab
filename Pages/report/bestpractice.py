import streamlit as st
from datetime import date
import pandas as pd
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, Date, MetaData, insert, select

class BestPractice:
    def __init__(self):
        # --- Connect to database ---
        self.engine = create_engine("sqlite:///best_practice.db", echo=False)
        self.metadata = MetaData()

        # --- Define table ---
        self.best_practice_table = Table(
            "best_practice",
            self.metadata,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("item", String(100)),
            Column("industry", String(100)),
            Column("country", String(100)),
            Column("quantity_tons", Float),
            Column("value_usd", Float),
            Column("export_date", Date)
        )

        # --- Create table if not exists ---
        self.metadata.create_all(self.engine)

    def show(self):
        st.title("🌍 Best Practiced Industry List")

        # -------- ADD FORM --------
        st.subheader("➕ Add New Industry Best Practice")

        with st.form("best_practice_form", clear_on_submit=True):
            export_item = st.text_input("Exported Item Name")
            industry = st.text_input("Exporting Industry Name")
            destination_country = st.text_input("Destination Country")
            quantity = st.number_input("Quantity (in tons)", min_value=0.0, step=0.1)
            value_usd = st.number_input("Export Value (in USD)", min_value=0.0, step=100.0)
            export_date = st.date_input("Date of Export", value=date.today())
            submit = st.form_submit_button("💾 Save Record")

        # -------- SAVE TO DATABASE --------
        if submit:
            with self.engine.connect() as conn:
                stmt = insert(self.best_practice_table).values(
                    item=export_item,
                    industry=industry,
                    country=destination_country,
                    quantity_tons=quantity,
                    value_usd=value_usd,
                    export_date=export_date
                )
                conn.execute(stmt)
                conn.commit()
            st.success(f"✅ Record for '{export_item}' saved successfully!")

        # -------- DISPLAY RECORDS --------
        st.divider()
        st.subheader("📦 Best Practice Records Summary")

        with self.engine.connect() as conn:
            result = conn.execute(select(self.best_practice_table)).fetchall()

        if result:
            df = pd.DataFrame(result, columns=[
                "ID", "Item", "Industry", "Country", "Quantity (tons)", "Value (USD)", "Export Date"
            ])
            st.dataframe(df, use_container_width=True)

            total_value = df["Value (USD)"].sum()
            total_quantity = df["Quantity (tons)"].sum()

            col1, col2 = st.columns(2)
            with col1:
                st.metric("💰 Total Export Value (USD)", f"${total_value:,.2f}")
            with col2:
                st.metric("📦 Total Quantity (tons)", f"{total_quantity:,.2f}")
        else:
            st.info("No best practice records yet. Add one using the form above.")
