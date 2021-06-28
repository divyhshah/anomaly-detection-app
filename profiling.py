import pandas as pd
import numpy as np
import pandas_profiling
import streamlit as st
from streamlit_pandas_profiling import st_profile_report

# Web App Title
def app():


    # Web App Title
    st.markdown('''
        # **The Data Insight App**

        This is the ***Data profiling app*** created in Streamlit using the ***pandas-profiling*** library.

        ---
        ''')

    # Upload CSV data
    with st.sidebar.header('1. Upload your CSV data'):
        uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv", "xlsx", "xls"])

    # Anomaly detection
    if uploaded_file is not None:
        @st.cache
        def load_csv():
            try:
                csv = pd.read_excel(uploaded_file)
            except:
                csv = pd.read_csv(uploaded_file)
            return csv
        df = load_csv()
        report = pandas_profiling.ProfileReport(df, explorative=True)
        st.header('**Input DataFrame Sample**')
        st.write(df.sample(20))
        st.header('**Data Profiling Report**')
        st_profile_report(report)
    else:
        st.info('Awaiting for CSV file to be uploaded.')
        if st.button('Press to use Example Dataset'):
            # Example data
            @st.cache
            def load_data():
                a = pd.DataFrame(
                    np.random.rand(100, 5),
                    columns=['a', 'b', 'c', 'd', 'e']
                )
                return a
            df = load_data()
            report = pandas_profiling.ProfileReport(df, explorative=True)
            st.header('**Input DataFrame Sample**')
            st.write(df.sample(20))
            st.header('**Data Profiling Report**')
            st_profile_report(report)

