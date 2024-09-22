import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
import time


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