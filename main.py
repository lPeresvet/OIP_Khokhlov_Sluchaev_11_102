import requests

outDir = "./out/"
indexMap = dict()

def writeToFile(body, number):
    try:
        with open(outDir+str(number), 'w', encoding='utf-8') as file:
            file.write(body)

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    # print(body)

def loadPage(url, number):
    resp = requests.get(url)

    print("Status Code:", resp.status_code)
    writeToFile(resp.text, number)

filename = "./input_sites_list.txt"

def writeIndexToFile():
    print("Записываю индексы...")
    indexFile = open(outDir + "index.txt", 'w', encoding='utf-8')
    for index in indexMap:
        indexEntry = "%d - %s\n" % (index, indexMap[index])
        indexFile.write(indexEntry)

    indexFile.close()
    print("Индексы записаны...")

try:
    file = open(filename, 'r', encoding='utf-8')

    line = file.readline()
    i = 1
    while line:
        print("Читаю: " + line.strip())
        loadPage(line.strip(), i)
        indexMap[i] = line.strip()

        line = file.readline()
        i += 1

    writeIndexToFile()

except Exception as e:
    print(f"Произошла ошибка: {e}")
finally:
    if 'file' in locals() and not file.closed:
        file.close()

