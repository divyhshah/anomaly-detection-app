import anomaly
import profiling
import streamlit as st
from footer import footer

PAGES = {"Data profiling": profiling,
         "Anomaly detection": anomaly}

# Page info
st.set_page_config(
        page_title="Data Insight",
        page_icon="https://image.flaticon.com/icons/png/512/4149/4149701.png",
        layout="wide",
    )


# Navigation
st.sidebar.subheader('Select feature you want to use')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()


# footer
footer()