from bs4 import BeautifulSoup
import requests
import time
import csv
import re


url = "https://www.goszakup.gov.kz/ru/search/announce?count_record=50&filter%5Bstatus%5D%5B0%5D=350&filter%5Bcustomer%5D="
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


for organization in organization_bins[4:]:
    # вытащить количество страниц
    time.sleep(2)
    response = requests.get(url + organization, verify=False)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find('ul', 'pagination').find_all('li')
    pagination_href = pagination[-1].a.get('href')
    reversed_pages = ''
    for i in pagination_href[::-1]:
        if i.isdigit():
            reversed_pages += i
        else:
            break

    if reversed_pages:
        pages = int(reversed_pages[::-1])
    else:
        pages = 1
    print('pages = ' + str(pages))
    rows_number = 0
    with open(f"{organization}.csv", mode="w", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=";",
                                 lineterminator="\r")
        file_writer.writerow(["№", 'id объявления', 'id лота', 'id пункта плана', 'Заказчик', 'Вид предмета закупок',
                              'Наименование закупаемых товаров, работ, услуг на государственном языке (в соответствии с КТРУ)',
                              'Дополнительная характеристика', 'Количество, объём', 'Единица измерения',
                              'Цена за единицу, тенге', 'Сумма, утвержденная для закупки, тенге',
                              'Начало приема заявок', 'Окончание приема заявок',
                              'Способ закупки', 'Статус лота',
                              ])
        file_writer.writerow([i for i in range(1, 17)])
        for page in range(1, pages+1):
            print('page = ' + str(page))
            appear_number = 0
            time.sleep(2)
            response = requests.get(url+organization+'&page='+str(page), verify=False)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            table = soup.find('table', id='search-result').tbody
            for table_row in table.find_all('tr'):
                appear_number += 1
                print('appear number = ' + str(appear_number))
                buying_method = ''
                subject_type = ''
                start_date = ''
                end_date = ''
                id_appear = ''

                columns = table_row.find_all('td')
                id_appear = columns[0].strong.text

                time.sleep(2)
                response = requests.get(url_base+columns[1].a['href'], verify=False)
                appear_html = response.text
                appear_soup = BeautifulSoup(appear_html, 'html.parser')

                appear_header = appear_soup.find('div', 'panel-default')
                header_inputs = appear_header.find_all('input')
                start_date = header_inputs[-2].get('value')
                end_date = header_inputs[-1].get('value')

                appear_body = appear_soup.find('div', 'tab-content').table.find_all('tr')
                for appear_info in appear_body:
                    if appear_info.th.text.strip() == 'Способ проведения закупки':
                        buying_method = appear_info.td.text.strip()
                    elif appear_info.th.text.strip() == 'Вид предмета закупок':
                        subject_type = appear_info.td.text.strip()

                lots_url = appear_soup.find('ul', 'nav-tabs').find_all('li')
                lots_url = lots_url[1].a.get('href')

                time.sleep(1)
                response = requests.get(url_base+columns[1].a['href']+lots_url, verify=False)
                lots_html = response.text
                lots_soup = BeautifulSoup(lots_html, 'html.parser')
                lots_info = lots_soup.find('div', 'tab-content')
                lots_body = lots_info.table.find_all('tr')

                if lots_body[0].th.next_sibling.next_sibling.text == 'Номер лота':
                    for lot in lots_body[1:]:
                        id_lot = ''
                        id_plan = ''
                        customer = ''
                        tru_name = ''
                        extra_character = ''
                        count = ''
                        measure = ''
                        one_price = ''
                        total_amount = ''
                        lot_status = ''

                        rows_number += 1
                        print('rows_number = ' + str(rows_number))

                        lot_data = lot.find_all('td')
                        lot_status = lot_data[-2].text.strip()
                        id_lot = lot_data[1].text.strip()
                        customer = lot_data[2].text.strip()
                        customer = re.sub(r'\s+', ' ', customer)
                        tru_name = lot_data[3].text.strip()
                        tru_name = re.sub(r'\s+', ' ', tru_name)
                        extra_character = lot_data[4].text.strip()
                        extra_character = re.sub(r'\s+', ' ', extra_character)
                        one_price = lot_data[5].text.strip()
                        count = lot_data[6].text.strip()
                        measure = lot_data[7].text.strip()
                        total_amount = lot_data[8].text.strip()

                        lot_row = [rows_number, id_appear, id_lot, id_plan, customer, subject_type, tru_name,
                                    extra_character, count, measure, one_price, total_amount, start_date, end_date,
                                    buying_method, lot_status]

                        file_writer.writerow(lot_row)
                else:
                    id_lot = lots_info.find('caption').p.contents[2].strip()
                    for lot in lots_body[1:]:
                        id_plan = ''
                        customer = ''
                        tru_name = ''
                        extra_character = ''
                        count = ''
                        measure = ''
                        one_price = ''
                        total_amount = ''
                        lot_status = ''

                        rows_number += 1
                        print('rows_number = ' + str(rows_number))

                        lot_data = lot.find_all('td')
                        id_plan = lot_data[1].text.strip()
                        lot_status = lot_data[-2].text.strip()
                        customer = lot_data[2].text.strip()
                        customer = re.sub(r'\s+', ' ', customer)
                        tru_name = lot_data[3].text.strip()
                        tru_name = re.sub(r'\s+', ' ', tru_name)
                        extra_character = lot_data[4].text.strip()
                        extra_character = re.sub(r'\s+', ' ', extra_character)
                        one_price = lot_data[5].text.strip()
                        count = lot_data[6].text.strip()
                        measure = lot_data[7].text.strip()
                        total_amount = lot_data[8].text.strip()

                        lot_row = [rows_number, id_appear, id_lot, id_plan, customer, subject_type, tru_name,
                                    extra_character, count, measure, one_price, total_amount, start_date, end_date,
                                    buying_method, lot_status]

                        file_writer.writerow(lot_row)