from bs4 import BeautifulSoup

def extract_page(path):
    with open(path) as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")

    body = soup.get_text(separator='\n', strip=True)

    return body