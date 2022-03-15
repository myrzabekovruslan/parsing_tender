from bs4 import BeautifulSoup
import requests
import time
import csv

url = "https://www.goszakup.gov.kz/ru/search/lots?filter%5Bcustomer%5D="
url_base = "https://www.goszakup.gov.kz"
organization_bins = ['081140019556', '000740001307', '990740002243',
                     '940740000911',
                     '960440000220',
                     '110340001853',
                     '020440003656',
                     '971040001050',
                     '050740004819',
                     '051040005150',
                     '100140011059',
                     '150540000186',
                     '000540000463',
                     '900640000128',
                     '120940001946',
                     '780140000023',
                    ]
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

pages = 9
appear_url = 'https://www.goszakup.gov.kz/ru/search/announce?filter%5Bcustomer%5D=210240033968+&count_record=50&page='
for page in range(1,pages+1):
    print(page)

    response = requests.get(appear_url+str(page), verify=False)
    time.sleep(2)


    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', id='search-result').tbody
    for row in table.find_all('tr'):
        columns = row.find_all('td')

        response = requests.get(url_base + columns[1].a['href'], verify=False)
        time.sleep(2)

        appear_html = response.text
        appear_soup = BeautifulSoup(appear_html, 'html.parser')

        appear_body = appear_soup.find('div', 'tab-content').table.find_all('tr')
        for appear_row in appear_body[::-1]:
            if appear_row.th.text == 'Признаки':
                print(appear_row.td.text)
                break


for organization in []:
    # вытащить количество страниц
    pages = 1
    lot_number = 0
    for page in range(pages):
        response = requests.get(url+organization, verify=False)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table', id='search-result').tbody
        for row in table.find_all('tr')[:1]:
            id_lot = ''
            id_appear = ''
            subject_type = ''
            tru_code = ''
            tru_name = ''
            extra_character = ''
            short_extra_character = ''
            count = ''
            one_price = ''
            total_amount = ''
            one_price_without_NDS = ''
            amount_without_NDS = ''
            amount_without_NDS_to_delivery = ''
            lot_status = ''
            plan_time_of_delivery = ''
            plan_time_of_buying = ''
            buying_method = ''
            contract_amount = ''
            economy = ''
            amount_of_delivery_payment = ''

            lot_number += 1
            columns = row.find_all('td')

            id_lot = columns[0].strong.text
            # print(columns[1].a['href'])
            # print(columns[2].a['href'])
            response = requests.get(url_base+columns[1].a['href'], verify=False)
            appear_html = response.text
            appear_soup = BeautifulSoup(appear_html, 'html.parser')

            appear_header = appear_soup.find('div', 'panel-default')
            id_appear = appear_header.find('div', 'form-group').input['value']

            appear_body = appear_soup.find('div', 'tab-content').table.find_all('tr')
            subject_type = appear_body[2].td.text
            buying_method = appear_body[0].td.text
            print(subject_type)


with open("classmates.csv", mode="w", encoding='utf-8') as w_file:
    # names = ["Имя", "Возраст"]
    file_writer = csv.writer(w_file, delimiter = ";",
                                 lineterminator="\r")
    # file_writer.writeheader()
    file_writer.writerow(["№", 'id объявления', 'id лота', 'Вид предмета закупок', 'Код товара, работы, услуги (в соответствии с КТРУ)',
                          'Наименование закупаемых товаров, работ, услуг на государственном языке (в соответствии с КТРУ)',
                          'Дополнительная характеристика', 'Краткая техническая характеристика', 'Количество, объём',
                          'Цена за единицу, тенге', 'Сумма, утвержденная  для закупки, тенге',
                          'Цена (без НДС) по договору, тенге',
                          'Сумма  (без НДС), договору тенге', 'Сумма (без НДС), оплачен поставщику тенге',
                          'Статус пункта плана', 'Планируемый срок осуществления поставки(месяц)',
                          'Планируемый срок осуществления государственных закупок(месяц)',
                          'Способ закупки',
                          'Сумма по договор факт', 'Экономия', 'Сумма оплаты поставщику'
                          ])
    file_writer.writerow([i for i in range(1,22)])
    # file_writer.writerow({"Имя": "Вова", "Возраст": "14"})