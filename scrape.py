import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup


# Takes in the website url and returns the content of the website
def scrape_website(website):
    print("Launching chrome browser...")


    chrome_driver_path = "./chromedriver" # the driver depends on the web-browser that someone is using
    options = webdriver.ChromeOptions() # enables me to specity how I want the driver to run (maybe I want it to ignore Images, maybe I want it to run in headless mode,...)
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options) # In this case I am using Chrome driver

    try:
        driver.get(website) # use the webdriver to go to the website
        print("Page loaded...")
        html = driver.page_source # Grab the page's html (the source page)

        return html
    
    finally:
        driver.quit()
        time.sleep(10)


def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser") # BeautifulSoup parses the html for me
    body_content = soup.body

    if body_content:
        return str(body_content)
    return "" # Incase there is no body content that was found.

# This functions cleans the bosy of the content removing unncessary tags like style tags for the css and also the script tags
def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract() # remove those tags

    clean_content = soup.get_text(separator="\n") # separate the text where those tags were removed with a newline
    cleaned_content = "\n".join(line.strip() for line in clean_content.splitlines() if line.strip()) # removes newlines that are unnecessary which mostly occurs when one grabs or scrapes content online.  This basically means that if there is no text between the \n and the next thing, just remove the newline

    return cleaned_content

# This function splits the cleaned content into chunks to align with the max tokens accepted by the llm
def split_dom_content(dom_content, max_length=6000): # we are creating batches of 6000 characters of the dom_content
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]