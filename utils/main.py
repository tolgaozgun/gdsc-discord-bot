import re
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def fix_regex(url: str):
    if url.startswith("http://"):
        url = url.replace("http://", "https://")
    if not url.startswith("https://"):
        url = "https://" + url
    return url

def match_regex(url):
    urls_to_match = [
        r'https://developers.google.com/profile/u/\w+',
        r'https://g.dev/\w+',
        r'http://developers.google.com/profile/u/\w+',
        r'http://g.dev/\w+']
    
    return any(re.match(url_to_match, url) for url_to_match in urls_to_match)

def email_exists_in_csv(email_to_check, filename='emails.csv'):
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if email_to_check.lower() in [field.lower() for field in row]:
                return True
    return False
