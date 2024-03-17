import json
import typing
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from tqdm import tqdm
import os

from db import add_badge_info_to_db
from utils.add_https_url import add_https_url
from utils.constants import BADGES
from utils.match_url import match_url




def scrape_badge(username: str, url: str):
    error_info = ""
    name = ""
    badge_count = 0
    badge_info = {badge: False for badge in BADGES}

    url = add_https_url(url)
    if not match_url(url):
        return {
            "error": "Invalid URL format",
            "name": name,
            "url": url,
            "badge_count": badge_count,
            "badges": [badge_info[badge] for badge in BADGES],
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        }
    
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract name
        name = soup.find('h1', class_='ql-display-small').get_text(strip=True)

        # Check for profile badges
        badges_found = soup.find_all('div', class_='profile-badge')
        if badges_found:
            error_info = ""
            for badge_div in badges_found:
                span = badge_div.find('span', class_='ql-title-medium')
                if span:
                    badge_name = span.get_text(strip=True)
                    if badge_name in BADGES:
                        badge_info[badge_name] = True
                        badge_count += 1
    except Exception as e:
        error_info = "Error fetching page"
        
    
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    badge_info = json.dumps(badge_info)
    
    add_badge_info_to_db(username, name, url, badge_info, badge_count, error_info, time)
        
    return {
        "error": error_info,
        "name": name,
        "url": url,
        "badge_count": badge_count,
        "badges": [badge_info[index] for index, badge in enumerate(BADGES)],
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    }

# scrape_badges accepts a dictionary where the key is the discord username and the value is the URL
async def scrape_badges(urls: typing.Dict[str, str], update_progress: typing.Callable[[int, int], None]):
    
    # for index, row in tqdm(urls, total=len(urls)):
    #     url = row[0]
    #     url = url.strip()
    #     result = scrape_badge(url)
    # Iterate through urls dictionary with tqdm and get the url and discord username for each entry
    issues = []
    total_count = len(urls)
    success_count = 0
    error_count = 0
    cur_count = 0
    for username, url in urls.items():
        cur_count += 1
        res = scrape_badge(username, url)
        if res['error']:
            error_count += 1
            issues.append("Username: " + username + " Error: (" + res['error'] + ") URL: <" + url + ">")
        else:
            success_count += 1
        await update_progress(cur_count, total_count, success_count, error_count)

    return issues, success_count