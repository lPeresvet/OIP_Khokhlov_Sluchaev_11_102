import unicodedata

from bs4 import BeautifulSoup

def extract_page(path):
    with open(path, encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")

    body = soup.get_text(separator=' ', strip=True)

    body = unicodedata.normalize("NFKD", body)
    body = "".join([c for c in body if unicodedata.category(c)[0] != "M"])
    body = body.encode("ascii", "ignore").decode("ascii")

    return body