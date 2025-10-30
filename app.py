import streamlit as st
from Pages.report import Rawmaterial, Performanceaudit, Export,BestPractice,Extension,Financialaudit,Grow,Importsubstitution,Infrustructure,Lease,NewIndustry,Productioncapacity,Rawmaterial,Workingcap
from Pages.industryprofile import IndustryProfile
from Pages.event import Event

class App:
    def __init__(self):
        # Each main page contains subpages (as class instances)
        self.pages = {
            "Report": {
                "Raw Material": Rawmaterial(),
                "Performance Audit": Performanceaudit(),
                "Export Report": Export(),
                "Best Practice":BestPractice(),
                "Industry Extension":Extension(),
                "Financial Audits": Financialaudit(),
                "የተሸጋገሩ": Grow(),
                "Import Substitution":Importsubstitution(),
                "Infrustructure":Infrustructure(),
                "Lease Finance":Lease(),
                "New Industry":NewIndustry(),
                "Production Capacity":Productioncapacity(),
                "Raw Material":Rawmaterial(),
                "Working capital":Workingcap()

            },
            "Industry Profile": IndustryProfile(),
            "Training & Event": Event(),
            "Contact": None  # Placeholder for now
        }

    def run(self):
        st.sidebar.title("📋 Main Menu")

        # Main choice
        main_choice = st.sidebar.radio(
            "Select Main Page",
            list(self.pages.keys()),
            key="main_menu"
        )

        # ------------------------------------------------
        # REPORT PAGE - expandable 22 subpages
        # ------------------------------------------------
        if main_choice == "Report":
            with st.sidebar.expander("📊 Report Subpages", expanded=True):
                sub_choice = st.radio(
                    "Choose Report Type",
                    list(self.pages["Report"].keys()),
                    key="report_subpage"
                )
            # Show selected subpage
            page = self.pages["Report"][sub_choice]
            page.show()

        # ------------------------------------------------
        # INDUSTRY PROFILE
        # ------------------------------------------------
        elif main_choice == "Industry Profile":
            st.sidebar.write("🏭 Industry Profile Section")
            self.pages["Industry Profile"].show()

        # ------------------------------------------------
        # TRAINING & EVENT
        # ------------------------------------------------
        elif main_choice == "Training & Event":
            st.sidebar.write("🎓 Training & Event Section")
            self.pages["Training & Event"].show()

        # ------------------------------------------------
        # CONTACT
        # ------------------------------------------------
        elif main_choice == "Contact":
            st.sidebar.info("📞 Contact Page Coming Soon...")

# --- Run the app ---
if __name__ == "__main__":
    App().run()
