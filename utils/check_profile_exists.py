

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def check_profile_exists(profile_url: str):
     # Check for devsite-profiles-splash--text class in the page
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    wd = webdriver.Chrome(options=options)
    wd.get(profile_url)
    time.sleep(8)  # Allow time for the page to load
    soup = BeautifulSoup(wd.page_source, 'lxml')
    wd.quit()  # Close the browser
    

    # Check for the presence of the specific class
    if soup.find_all('div', {'class': 'devsite-profiles-splash--text'}):
        return True
    return False