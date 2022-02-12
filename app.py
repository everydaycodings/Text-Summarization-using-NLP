from prometheus_client import Summary
import streamlit as st
from helper import get_summary


st.set_page_config(
     page_title="Data Analysis Web App",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://github.com/everydaycodings/Data-Analysis-Web-App',
         'Report a bug': "https://github.com/everydaycodings/Data-Analysis-Web-App/issues/new",
         'About': "# This is a header. This is an *extremely* cool app!"
     }
)


st.sidebar.title("Text Summarization Web App")

option = ["Custom Text Summarization", "News Summary and Headlines"]
choice = st.sidebar.selectbox("Select of your choice", options=option)


if choice == "Custom Text Summarization":
    st.title("Welcome to {}".format(choice))

    col1, col2 = st.columns(2)

    with col1:
        text = st.text_area(label="Enter Your Text or story", height=350, placeholder="Enter Your Text or story or your article iit can be of any length")
        
        if st.button("Get Summary and Headline"):
            summary = get_summary(text)
    
            with col2:
                try:
                    st.write("Text Summary (Summary length: {})".format(len(summary)))
                    st.code(summary)
                    st.write("Text Headline")
                    st.code(len(text))
                except NameError:
                    pass