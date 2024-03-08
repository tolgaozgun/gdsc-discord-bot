def add_https_url(url: str):
    if url.startswith("http://"):
        url = url.replace("http://", "https://")
    if not url.startswith("https://"):
        url = "https://" + url
    return url