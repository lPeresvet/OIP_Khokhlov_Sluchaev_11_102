import requests
from bs4 import BeautifulSoup

init_page = "https://www.geeksforgeeks.org/python-program-crawl-web-page-get-frequent-words/"
response = requests.get(init_page)
page = str(BeautifulSoup(response.content, features="html.parser"))


def getURL(page):

    start_link = page.find("a href")
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1: end_quote]
    return url, end_quote

while True:
    url, n = getURL(page)
    page = page[n:]
    if url:
        if url.startswith("http"):
            print(url.split("?")[0])
    else:
        break