import re
import string
import unicodedata

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

punctuation = re.escape(string.punctuation)  # Экранируем спецсимволы
pattern = r"[" + punctuation + "]"


def tokenize_and_clean(input):
    tokens = word_tokenize(input.lower())

    stop_words = set(stopwords.words('english'))
    filtered_tokens = [w for w in tokens if not w in stop_words]

    unique_tokens = set()
    for token in filtered_tokens:
        if not re.search(r"\b[a-z]+\b", token):
            continue
        if re.search(pattern, token):
            continue
        if len(token) == 1:
            continue

        unique_tokens.add(token)

    return list(unique_tokens)


def tokenize(input):
    tokens = tokenize_and_clean(input)
    tokens.sort()

    return tokens