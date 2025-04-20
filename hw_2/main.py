import os

from page_payload_extractor import *
from tokens_parser import *
import subprocess
from nltk.stem import WordNetLemmatizer
import nltk

pages_num = 155
outDir = "../out"

try:
    result = subprocess.run(["./cleanup_hw_2.sh"], capture_output=True, text=True, check=True)
    print("Стандартный вывод:", result.stdout)

except subprocess.CalledProcessError as e:
    print("Очистка заввершилась с ошибкой:", e)

lemmatizer = WordNetLemmatizer()

def lemmas_to_str(lemmas):
    res = []
    for lemma in lemmas:
        value = lemmas[lemma]

        res.append(" ".join(value))

    return "\n".join(res)

def proceed_file(file):
    print("Обработка файла", file)
    out_file = open(outDir + "/tokens/tokens_"+str(file)+".txt", 'w', encoding='utf-8')

    extracted_text = extract_page("../out/" + str(file))

    tokens = tokenize(extracted_text)

    # print(tokens)

    out_file.write("\n".join(tokens))
    out_file.close()

    lemmas_file = open(outDir + "/tokens/lemmas_" + str(file) + ".txt", 'w', encoding='utf-8')

    tagged_tokens = nltk.pos_tag(tokens)

    lemma_groups = {}

    for token, tag in tagged_tokens:
        if tag.startswith('J'):
            pos = 'a'
        elif tag.startswith('V'):
            pos = 'v'
        elif tag.startswith('N'):
            pos = 'n'
        elif tag.startswith('R'):
            pos = 'r'
        else:
            pos = 'n'

        lemma = lemmatizer.lemmatize(token, pos=pos)
        if lemma in lemma_groups:
            lemma_groups[lemma].append(token)
        else:
            lemma_groups[lemma] = [token]

    # print(lemma_groups)

    lemmas_file.write(lemmas_to_str(lemma_groups))

    lemmas_file.close()
    print("Завершена обработка файла", file)

nltk.download('all')
os.mkdir(outDir + "/tokens")

for i in range(1, pages_num+1):
    proceed_file(i)
