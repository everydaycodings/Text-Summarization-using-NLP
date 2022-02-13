from prometheus_client import Summary
import streamlit as st
from helper import get_summary, spacy_rander, fetch_news, fetch_news_links


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

        try:
            with col2:
                st.write("Text Summary (Summary length: {})".format(len(summary)))
                st.code(summary)
                st.write("Text Headline")
                st.code(len(text))

            rend = spacy_rander(summary)
            
        except NameError:
            pass

if choice == "News Summary and Headlines":
    st.title("BBC News Summary")

    link, title, thumbnail = fetch_news_links()
    fetch_news = fetch_news()
    
    col1, col2 = st.columns(2)

    with col1:
        for i in range(len(link)):
            if (i % 2) == 0:
                st.image(thumbnail[i])
                st.write(title[i])
                with st.expander("Read The Summary"):
                    st.write(get_summary(fetch_news[i]))
                st.markdown("[**Read Full Article**]({})".format(link[i]), unsafe_allow_html=True)
    
    with col2:
        for i in range(len(link)):
            if (i % 2) != 0:
                st.image(thumbnail[i])
                st.write(title[i])
                with st.expander("Read The Summary"):
                    st.write(get_summary(fetch_news[i]))
                st.markdown("[**Read Full Article**]({})".format(link[i]), unsafe_allow_html=True)