

import requests
from bs4 import BeautifulSoup

def check_profile_exists(profile_url: str):
    response = requests.get(profile_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract name
    name = soup.find('h1', class_='ql-display-small').get_text(strip=True)
    
    if name:
        return True
    return False