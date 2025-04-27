import requests
import threading
import subprocess

outDir = "./out/"
indexMap = dict()
filename = "./input_sites_list.txt"
threads = []
cleanup_script_path = "./cleanup.sh"

try:
    result = subprocess.run([cleanup_script_path], capture_output=True, text=True, check=True)
    print("Стандартный вывод:", result.stdout)

except subprocess.CalledProcessError as e:
    print("Очистка заввершилась с ошибкой:", e)

def writeToFile(body, number):
    try:
        with open(outDir+str(number)+".html", 'w', encoding='utf-8') as file:
            file.write(body)

    except Exception as e:
        print(f"Произошла ошибка: {e}")

def loadPage(url, number):
    print("Читаю: " + url)

    resp = requests.get(url)

    print(url, " response code:", resp.status_code)
    writeToFile(resp.text, number)


def writeIndexToFile():
    print("Записываю индексы...")
    indexFile = open(outDir + "index.txt", 'w', encoding='utf-8')
    for index in indexMap:
        indexEntry = "%d - %s\n" % (index, indexMap[index])
        indexFile.write(indexEntry)

    indexFile.close()
    print("Индексы записаны")

try:
    file = open(filename, 'r', encoding='utf-8')

    line = file.readline()
    i = 1
    while line:
        indexMap[i] = line.strip()

        thread = threading.Thread(target=loadPage, args=(line.strip(),i,))
        threads.append(thread)
        thread.start()

        line = file.readline()
        i += 1

    for thread in threads:
        thread.join()

    writeIndexToFile()

except Exception as e:
    print(f"Произошла ошибка: {e}")
finally:
    if 'file' in locals() and not file.closed:
        file.close()

