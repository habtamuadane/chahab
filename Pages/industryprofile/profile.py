import streamlit as st
import pandas as pd

class IndustryProfile:
    def __init__(self):
        if "profiles" not in st.session_state:
            st.session_state["profiles"] = []

    def show_profile_page(self):
        st.title("🏭 Industry Profile")

        menu = st.radio("Choose Option", ["Add Profile", "View Profiles"])

        if menu == "Add Profile":
            name = st.text_input("Industry Name")
            zone = st.selectbox("Zone", ["Bahir Dar", "West Gojjam", "East Gojjam"])
            sector = st.text_input("Sector")
            employees = st.number_input("Number of Employees", min_value=1)

            if st.button("Save Profile"):
                st.session_state["profiles"].append({
                    "Name": name, "Zone": zone, "Sector": sector, "Employees": employees
                })
                st.success("Profile added successfully!")

        elif menu == "View Profiles":
            df = pd.DataFrame(st.session_state["profiles"])
            st.dataframe(df)
            if not df.empty:
                st.download_button("Download Profiles", df.to_csv(index=False), "profiles.csv")
