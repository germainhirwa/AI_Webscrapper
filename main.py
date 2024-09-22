import streamlit as st

st.title("GermAI Web Scraper")
url = st.text_input("Enter a Website URL: ")

if st.button("Scrape Site"):
    st.write("Scraping the website")
