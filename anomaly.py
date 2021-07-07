import pandas as pd
import io
import os
import base64
import streamlit as st
from pycaret.anomaly import *

def app():

    # Web App Title
    st.markdown('''
    # **The Data Insight App**
    
    This is the ***Anomaly detection app*** helps you to find outlier in the dataset.
    
    ---
    ''')

    # Upload CSV data
    with st.sidebar.header('1. Upload your CSV data'):
        uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv", "xlsx", "xls"])

    if uploaded_file is not None:
        @st.cache
        def load_csv():
            try:
                csv = pd.read_excel(uploaded_file)
            except:
                csv = pd.read_csv(uploaded_file)
            return csv
        df = load_csv()

        st.header('**Input DataFrame Sample**')
        st.write(df.sample(20))

        # target column selection
        df = df.select_dtypes('number')
        columns = df.columns.tolist()
        target_column = st.sidebar.selectbox('Select your target column:', columns)

        # shortlist column based on correlation with taget
        corr = df.corr()
        cor_target = abs(corr[target_column])
        relevan_cols = cor_target[cor_target>=0.2].index
        df = df[relevan_cols]

        # Anomaly detection
        try:
            s = setup(df, session_id=123, silent=True)
            iforest = create_model('iforest', fraction=0.1)
            iforest_results = assign_model(iforest)
            anomaly = iforest_results[iforest_results['Anomaly'] == 1]
            anomaly = anomaly.drop('Anomaly', axis=1)
            st.write('---')
            st.header('**Data contains Anomaly**')
            st.write(anomaly.head(10))
            st.text(f"Total {anomaly.shape[0]} anomalies found")
            towrite = io.BytesIO()
            downloaded_file = anomaly.to_excel(towrite, encoding='utf-8', index=False, header=True)
            towrite.seek(0)  # reset pointer
            b64 = base64.b64encode(towrite.read()).decode()  # some strings
            linko = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="anomaly.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
        except:
            st.markdown('<font color="red">Please select another target column</font>', unsafe_allow_html=True)

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
            s = setup(df, session_id=123, silent=True)
            iforest = create_model('iforest', fraction=0.1)
            iforest_results = assign_model(iforest)
            anomaly = iforest_results[iforest_results['Anomaly'] == 1]
            st.header('**Input DataFrame**')
            st.write(df)
            st.write('---')
            st.header('**Data contains Anomaly**')
            st.write(anomaly.head(10))
