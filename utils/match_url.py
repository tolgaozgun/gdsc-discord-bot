import re

def match_url(url):
    urls_to_match = [
        r'https://www\.cloudskillsboost\.google/public_profiles/.+',
        r'http://www\.cloudskillsboost\.google/public_profiles/.+'
    ]
    return any(re.match(url_to_match, url) for url_to_match in urls_to_match)
