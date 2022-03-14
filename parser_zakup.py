from bs4 import BeautifulSoup
import requests
import time
import csv

url = "https://www.goszakup.gov.kz/ru/search/lots"
url_base = "https://www.goszakup.gov.kz"
# page = ''
# while page == '':
#     try:
#         page = requests.get(url, verify=False)
#         break
#     except:
#         print("Connection refused by the server..")
#         print("Let me sleep for 5 seconds")
#         print("ZZzzzz...")
#         time.sleep(5)
#         print("Was a nice sleep, now let me continue...")
#         continue
# print(page.text)

response = requests.get(url, verify=False)
html = response.text
soup = BeautifulSoup(html, 'html.parser')
table = soup.find('table', id='search-result').tbody
for row in table.find_all('tr')[:1]:
    two_links = row.find_all('td')
    print(two_links[1].a['href'])
    print(two_links[2].a['href'])
    response = requests.get(url_base+two_links[1].a['href'], verify=False)
    print(response.text)

with open("classmates.csv", mode="w", encoding='utf-8') as w_file:
    names = ["Имя", "Возраст"]
    file_writer = csv.writer(w_file, delimiter = ";",
                                 lineterminator="\r")
    # file_writer.writeheader()
    file_writer.writerow(["dw", 2])
    # file_writer.writerow({"Имя": "Маша", "Возраст": "15"})
    # file_writer.writerow({"Имя": "Вова", "Возраст": "14"})