import re

def match_url(url):
    urls_to_match = [
        r'https://developers.google.com/profile/u/\w+',
        r'https://g.dev/\w+',
        r'http://developers.google.com/profile/u/\w+',
        r'http://g.dev/\w+']
    
    return any(re.match(url_to_match, url) for url_to_match in urls_to_match)