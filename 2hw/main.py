import os

from page_payload_extractor import *
import subprocess
# from nltk.tokenize import word_tokenize
# import nltk
#
# nltk.download('stopwords')
# text = 'Надеюсь, дождь не помешает веселью'
# tokenize = word_tokenize(text)
# print(tokenize)

pages_num = 155
outDir = "../out"

try:
    result = subprocess.run(["../cleanup_hw2.sh"], capture_output=True, text=True, check=True)
    print("Стандартный вывод:", result.stdout)

except subprocess.CalledProcessError as e:
    print("Очистка заввершилась с ошибкой:", e)


def proceed_file(file):
    print("Обработка файла", file)
    os.mkdir(outDir + "/" + str(file) + "_tokens")
    out_file = open(outDir + "/" + str(file) + "_tokens/text.txt", 'w', encoding='utf-8')

    extracted_text = extract_page("../out/" + str(file))
    # todo extract tokens from this text

    out_file.write(extracted_text)
    out_file.close()
    print("Завершена обработка файла", file)


for i in range(1, pages_num+1):
    proceed_file(i)

