from .rawmaterial import Rawmaterial
from .performanceaudit import Performanceaudit
from .export import Export
from .bestpractice import BestPractice
from.extension import Extension
from .financialaudit import Financialaudit
from.grow import Grow
from .importsubstitution import Importsubstitution
from .infrustructure import Infrustructure
from .lease import Lease
from .newindustry import NewIndustry
from .productioncapacity import Productioncapacity
from .rawmaterial import Rawmaterial
from .workingcapital import Workingcap

import streamlit as st


class Report:
    def __init__(self):
        self.sub_pages = [
           ("Raw Material",Rawmaterial()),
            ("Performance Audit",Performanceaudit()),
            ("Export Report",Export()),
            ("Best Practice",BestPractice()),
            ("Industry Extension",Extension()),
            ("Financial Audits", Financialaudit()),
            ("የተሸጋገሩ", Grow()),
            ("Import Substitution",Importsubstitution()),
            ("Infrustructure",Infrustructure()),
            ("Lease Finance",Lease()),
            ("New Industry",NewIndustry()),
            ("Production Capacity",Productioncapacity()),
            ("Raw Material",Rawmaterial()),
            ("Working capital",Workingcap()),
            ("Export", Export()),
        ]

    def show_report_pages(self):
        st.title("📑 Reports Section")
        subchoice = st.sidebar.radio("Select report type:", [s[0] for s in self.sub_pages])

        for name, page in self.sub_pages:
            if subchoice == name:
                page.display()
                break
