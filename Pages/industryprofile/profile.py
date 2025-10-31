import streamlit as st
import pandas as pd
import sqlite3
import io
from datetime import datetime
from constants import ZONES
from sector import SECTOR
from ilicense import ILICENCE
from tlicence import TLICENCE
from ownership import OWNERSHIP
from level import LEVEL
from source import SOURCE
from product import PRODUCT
from audit import AUDIT
from quality import QUALITY

class IndustryProfile:
    DB_FILE = "industry_profiles.db"

    def __init__(self):
        # Ensure database table exists
        with sqlite3.connect(self.DB_FILE) as conn:
            c = conn.cursor()
            c.execute("""
                CREATE TABLE IF NOT EXISTS profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    owner TEXT,
                    nationality TEXT,
                    land INTEGER,
                    sector TEXT,
                    mainproduct TEXT,
                    ilicense TEXT,
                    tlicence TEXT,
                    tin INTEGER,
                    establish DATE,
                    prodstart DATE,
                    startup REAL,
                    capital REAL,
                    formation TEXT,
                    level TEXT,
                    source TEXT,
                    zone TEXT,
                    wereda TEXT,
                    ketema TEXT,
                    phone1 TEXT,
                    phone2 TEXT,
                    product TEXT,
                    audit TEXT,
                    quality TEXT,
                    permanent_male INTEGER,
                    permanent_female INTEGER,
                    temporary_male INTEGER,
                    temporary_female INTEGER,
                    indstatus TEXT,
                    entry_year INTEGER
                )
            """)
            conn.commit()

    def add_profile(self, name, owner, nationality, land, sector, mainproduct, ilicense, tlicence, tin,
                    establish, prodstart, startup, capital, formation, level, source, zone, wereda, ketema,
                    phone1, phone2, product, audit, quality,
                    permanent_male, permanent_female, temporary_male, temporary_female, indstatus):
        entry_year = datetime.now().year
        with sqlite3.connect(self.DB_FILE) as conn:
            c = conn.cursor()
            c.execute("""
                INSERT INTO profiles (name, owner, nationality, land, sector, mainproduct, ilicense, tlicence, tin,
                                      establish, prodstart, startup, capital, formation, level, source, zone, wereda, ketema,
                                      phone1, phone2, product, audit, quality,
                                      permanent_male, permanent_female, temporary_male, temporary_female, indstatus, entry_year)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, owner, nationality, land, sector, mainproduct, ilicense, tlicence, tin,
                  establish, prodstart, startup, capital, formation, level, source, zone, wereda, ketema,
                  phone1, phone2, product, audit, quality,
                  permanent_male, permanent_female, temporary_male, temporary_female, indstatus, entry_year))
            conn.commit()

    def get_profiles(self):
        with sqlite3.connect(self.DB_FILE) as conn:
            df = pd.read_sql("SELECT * FROM profiles", conn)
        return df

    def show(self):
        st.title("🏭 Industry Profile")

        menu = st.radio("Choose Option", ["Add Profile", "View Profiles", "Summary"])

        if menu == "Add Profile":
            with st.expander("➕ Add New Industry Profile", expanded=True):
            # --- Input fields ---
                name = st.text_input("የአምራች ኢንዱስትሪው ስም")
                owner = st.text_input("የባለቤት / ተወካይ ስም")
                nationality = st.text_input("ዜግነት")
                land = st.number_input("የመሬት መጠን (በሄክታር)", min_value=0)
                sector = st.selectbox("የተሰማራበት ዘርፍ", SECTOR)
                mainproduct = st.text_input("ዋና የምርት ዓይነት")
                ilicense = st.selectbox("የኢንቨስትመንት ፈቃድ", ILICENCE)
                tlicence = st.selectbox("የንግድ ፈቃድ", TLICENCE)
                tin = st.text_input("የግብር መለያ ቁጥር")
                establish = st.date_input("የተቋቋመበት ዓ.ም")
                prodstart = st.date_input("ምርት የጀመረበት ዓ.ም")
                startup = st.number_input("መነሻ ካፒታል (ብር)", min_value=0.0, format="%.2f")
                capital = st.number_input("ወቅታዊ ጠቅላላ ሃብት (ብር)", min_value=0.0, format="%.2f")
                formation = st.selectbox("የአደረጃጀት ዓይነት", OWNERSHIP)
                level = st.selectbox("ደረጃ", LEVEL)
                source = st.selectbox("የሀብት ምንጭ", SOURCE)
                zone = st.selectbox("ዞን/ከተማ", ZONES)
                wereda = st.text_input("ወረዳ")
                ketema = st.text_input("ከተማ")
                phone1 = st.text_input("📞 ስልክ ቁጥር", placeholder="+2519XXXXXXXX")
                phone2 = st.text_input("📞 ስልክ ቁጥር 2", placeholder="+2519XXXXXXXX")
                product = st.selectbox("የምርት ዓይነት", PRODUCT)
                audit = st.selectbox("አዲስ እትም", AUDIT)
                quality = st.selectbox("የምርት ጥራት", QUALITY)
                permanent_male = st.number_input("Permanent Male Employees", min_value=0, step=1)
                permanent_female = st.number_input("Permanent Female Employees", min_value=0, step=1)
                temporary_male = st.number_input("Temporary Male Employees", min_value=0, step=1)
                temporary_female = st.number_input("Temporary Female Employees", min_value=0, step=1)
                indstatus = st.selectbox("ኢንዱስትሪ ሁኔታ", ["ምርት ላይ", "ለጊዜው ቆመ", "ማምረት ያቋረጠ"])

            if st.button("Save Profile"):
                self.add_profile(
                    name, owner, nationality, land, sector, mainproduct, ilicense, tlicence, tin,
                    establish, prodstart, startup, capital, formation, level, source, zone, wereda, ketema,
                    phone1, phone2, product, audit, quality,
                    permanent_male, permanent_female, temporary_male, temporary_female, indstatus
                )
                st.success("✅ Profile added successfully!")

        elif menu == "View Profiles":
            df = self.get_profiles()
            if not df.empty:
                st.dataframe(df.drop(columns=["id"], errors="ignore"))
                # Filter by entry year
                years = df['entry_year'].dropna().unique()
                selected_year = st.selectbox("Choose Year to Download", sorted(years, reverse=True))
                filtered_df = df[df['entry_year'] == selected_year]

                # Convert filtered DataFrame to Excel
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
                    filtered_df.drop(columns=["id"], errors="ignore").to_excel(writer, index=False, sheet_name="Profiles")

                st.download_button(
                    label=f"📥 Download Profiles Entered in {selected_year}",
                    data=buffer.getvalue(),
                    file_name=f"industry_profiles_{selected_year}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.info("No profiles found. Add a profile first.")

        elif menu == "Summary":
            df = self.get_profiles()
            if df.empty:
                st.info("No profiles found. Add a profile first.")
                return

            st.subheader("📊 Comprehensive Summary")

            # --- Group by Zone, Level, Sector ---
            group_cols = ["zone", "level", "sector"]
            summary_df = df.groupby(group_cols).agg(
                total_profiles=pd.NamedAgg(column="id", aggfunc="count"),
                permanent_male=pd.NamedAgg(column="permanent_male", aggfunc="sum"),
                permanent_female=pd.NamedAgg(column="permanent_female", aggfunc="sum"),
                temporary_male=pd.NamedAgg(column="temporary_male", aggfunc="sum"),
                temporary_female=pd.NamedAgg(column="temporary_female", aggfunc="sum")
            ).reset_index()

            st.dataframe(summary_df)

            # Optional: download summary
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
                summary_df.to_excel(writer, index=False, sheet_name="Summary")
            st.download_button(
                label="📥 Download Summary as Excel",
                data=buffer.getvalue(),
                file_name="industry_summary.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )


# Run the app
if __name__ == "__main__":
    profile_app = IndustryProfile()
    profile_app.show()
