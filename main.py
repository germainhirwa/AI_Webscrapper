import streamlit as st
from scrape import (
    scrape_website, 
    split_dom_content, 
    clean_body_content, 
    extract_body_content,
)

st.title("GermAI Web Scraper")
url = st.text_input("Enter a Website URL: ")

if st.button("Scrape Site"):
    st.write("Scraping the website")
    
    result = scrape_website(url)
    body_content = extract_body_content(result)
    cleaned_content = clean_body_content(body_content)

    st.session_state.dom_content = cleaned_content # this enables us to access it later

    with st.expander("View Dom Content"): # a button that when clicked allows us to expand and view content in the text_area. Can also collapse it when clicked
        st.text_area("DOM Content", cleaned_content, height=300) # I gave the text_area a default of 300 but can be expanded by scrolling
