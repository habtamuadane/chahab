import streamlit as st
import pandas as pd
from datetime import date

class Event:
    def __init__(self):
        if "events" not in st.session_state:
            st.session_state["events"] = []

    def show_event_page(self):
        st.title("🎓 Training & Events")

        tab1, tab2 = st.tabs(["Add Event", "View Events"])

        with tab1:
            title = st.text_input("Event Title")
            location = st.text_input("Location")
            start_date = st.date_input("Start Date")
            end_date = st.date_input("End Date")
            participants = st.text_area("Participants (comma separated)")

            if st.button("Save Event"):
                st.session_state["events"].append({
                    "Title": title,
                    "Location": location,
                    "Start Date": start_date,
                    "End Date": end_date,
                    "Participants": [p.strip() for p in participants.split(",") if p.strip()]
                })
                st.success("Event added!")

        with tab2:
            if not st.session_state["events"]:
                st.info("No events yet.")
            else:
                df = pd.DataFrame(st.session_state["events"])
                st.dataframe(df)
                st.download_button("📥 Download Events", df.to_csv(index=False), "events.csv")
