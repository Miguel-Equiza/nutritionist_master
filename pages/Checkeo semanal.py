import streamlit as st
import pandas as pd

uploaded_file = st.file_uploader("Choose a file", type="xlsx")

if uploaded_file is not None:
    # Read the Excel file into a DataFrame
    df = pd.read_excel(uploaded_file)

st.write("Here are your inputs:")
st.dataframe(df)
