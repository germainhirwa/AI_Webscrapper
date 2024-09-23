import streamlit as st
from scrape import (
    scrape_website, 
    split_dom_content, 
    clean_body_content, 
    extract_body_content,
)

from parse import parse_with_ollama

# The streamlit UI
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


if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe want you want to parse?") # Asking the user for their input/prompt

    if st.button("Parse Content"): # If this button is clicked
        if parse_description: # If the user offered the prompt of what they want to parse
            st.write("Parsing the content")

            dom_chunks = split_dom_content(st.session_state.dom_content)
            # Then I have to pass the chunks and the prompt into the llm to be parsed and then write the result
            result = parse_with_ollama(dom_chunks, parse_description) # parsing with ollama's llama3.1 model which has 8B parameters

            st.write(result) # Then write the results