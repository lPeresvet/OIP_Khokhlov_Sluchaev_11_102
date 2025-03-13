import requests

def loadPage(url):
    resp = requests.get(url)

    print("Status Code:", resp.status_code)

    print("\nResponse Content:")
    print(resp.text)

filename = "./input_sites_list.txt"

try:
    file = open(filename, 'r', encoding='utf-8')


    line = file.readline()
    while line:
        print("Читаю: " + line.strip())
        loadPage(line.strip())

        line = file.readline()


except Exception as e:
    print(f"Произошла ошибка: {e}")
finally:
    if 'file' in locals() and not file.closed:
        file.close()

