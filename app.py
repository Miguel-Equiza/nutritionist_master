import streamlit as st

st.markdown(
    """
    # This is a header
    ## This is a subheader
    This is text

    """
)

uploaded_file = st.file_uploader("Choose a file", type="xlsx")

if uploaded_file:
    st.write(f"Filename: {uploaded_file.name}")
    content = uploaded_file.read()
    st.write(content)
