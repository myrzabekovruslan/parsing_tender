from bs4 import BeautifulSoup
import requests
import time
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait



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

# pages = 9
# appear_url = 'https://www.goszakup.gov.kz/ru/search/announce?filter%5Bcustomer%5D=210240033968+&count_record=50&page='
# for page in range(1,pages+1):
#     print(page)
#
#     response = requests.get(appear_url+str(page), verify=False)
#     time.sleep(2)
#
#
#     html = response.text
#     soup = BeautifulSoup(html, 'html.parser')
#     table = soup.find('table', id='search-result').tbody
#     for row in table.find_all('tr'):
#         columns = row.find_all('td')
#
#         response = requests.get(url_base + columns[1].a['href'], verify=False)
#         time.sleep(2)
#
#         appear_html = response.text
#         appear_soup = BeautifulSoup(appear_html, 'html.parser')
#
#         appear_body = appear_soup.find('div', 'tab-content').table.find_all('tr')
#         for appear_row in appear_body[::-1]:
#             if appear_row.th.text == 'Признаки':
#                 print(appear_row.td.text)
#                 break


for organization in organization_bins[:1]:
    # вытащить количество страниц
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

    pages = int(reversed_pages[::-1])
    print('pages = ' + str(pages))
    rows_number = 0
    with open(f"{organization}.csv", mode="w", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=";",
                                 lineterminator="\r")
        file_writer.writerow(["№", 'id объявления', 'id лота', 'id пункта плана', 'Вид предмета закупок',
                              'Код товара, работы, услуги (в соответствии с КТРУ)',
                              'Наименование закупаемых товаров, работ, услуг на государственном языке (в соответствии с КТРУ)',
                              'Дополнительная характеристика', 'Краткая техническая характеристика',
                              'Количество, объём',
                              'Цена за единицу, тенге', 'Сумма, утвержденная  для закупки, тенге',
                              'Цена (без НДС) по договору, тенге',
                              'Сумма  (без НДС), договору тенге', 'Сумма (без НДС), оплачен поставщику тенге',
                              'Начало приема заявок', 'Окончание приема заявок',
                              'Планируемый срок осуществления поставки',
                              'Способ закупки', 'Статус лота',
                              'Сумма по договору факт', 'Экономия', 'Сумма оплаты поставщику'
                              ])
        file_writer.writerow([i for i in range(1, 24)])
        for page in range(1, pages+1):
            print('page = ' + str(page))
            time.sleep(1)
            response = requests.get(url+organization+'&page='+str(page), verify=False)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            table = soup.find('table', id='search-result').tbody
            # print(table)
            for table_row in table.find_all('tr'):
                buying_method = ''
                subject_type = ''
                start_date = ''
                end_date = ''
                id_appear = ''

                columns = table_row.find_all('td')
                # id_lot = columns[0].strong.text
                id_appear = columns[0].strong.text

                # lot_status = columns[-1].text

                time.sleep(1)
                response = requests.get(url_base+columns[1].a['href'], verify=False)
                appear_html = response.text
                appear_soup = BeautifulSoup(appear_html, 'html.parser')

                appear_header = appear_soup.find('div', 'panel-default')
                header_inputs = appear_header.find_all('input')
                start_date = header_inputs[-2].get('value')
                end_date = header_inputs[-1].get('value')

                appear_body = appear_soup.find('div', 'tab-content').table.find_all('tr')
                subject_type = appear_body[2].td.text
                buying_method = appear_body[0].td.text

                lots_url = appear_soup.find('ul', 'nav-tabs').find_all('li')
                lots_url = lots_url[1].a.get('href')

                time.sleep(1)
                response = requests.get(url_base+columns[1].a['href']+lots_url, verify=False)
                lots_html = response.text
                lots_soup = BeautifulSoup(lots_html, 'html.parser')
                lots_body = lots_soup.find('div', 'tab-content').table.find_all('tr')

                driver = webdriver.Chrome(executable_path=r'C:\Users\tengri\Downloads\chromedriver_win32\chromedriver.exe')
                if lots_body[0].th.next_sibling.next_sibling.text == 'Номер лота':
                    for lot in lots_body[1:]:
                        id_lot = ''
                        id_plan = ''

                        tru_code = ''
                        tru_name = ''
                        extra_character = ''
                        short_tech_character = ''
                        count = ''
                        one_price = ''
                        total_amount = ''
                        one_price_without_NDS = ''
                        amount_without_NDS = ''
                        amount_without_NDS_to_delivery = ''

                        plan_time_of_delivery = ''
                        lot_status = ''
                        fact_amount = ''
                        economy = ''
                        amount_of_delivery_payment = ''

                        rows_number += 1
                        print('rows_number = ' + str(rows_number))
                        nid_lot = lot.a.get('data-lot-id')
                        lot_status = lot.find_all('td')[-2].text
                        # print(lot_status)
                        # response = requests.get(url_base + columns[1].a['href'] + lots_url + lot_url, verify=False)
                        # lot_html = response.text
                        # lot_soup = BeautifulSoup(lot_html, 'html.parser')
                        # lot_body = lot_soup.find('div', 'modal-lot-content').table.find_all('tr')
                        # print(lot_body)
                        try:
                            time.sleep(1)
                            driver.get(url_base + columns[1].a['href'] + lots_url)
                            driver.find_element_by_xpath(f"//a[@data-lot-id='{nid_lot}']").click()
                            wait = WebDriverWait(driver, timeout=5)
                        except:
                            pass
                        # print(driver.page_source)
                        lot_soup = BeautifulSoup(driver.page_source, 'html.parser')
                        lot_body = lot_soup.find('div', 'modal-lot-content').table.find_all('tr')
                        for row in lot_body:
                            # if row.th.text == 'Дата начала приема заявок':
                            #     start_date = row.td.text
                            # elif row.th.text == 'Дата окончания приема заявок':
                            #     end_date = row.td.text
                            if row.th.text == 'Код ТРУ':
                                tru_code = row.td.text
                            elif row.th.text == 'Лот №':
                                id_lot = row.td.text
                            elif row.th.text == 'Наименование ТРУ':
                                tru_name = row.td.text
                            elif row.th.text == 'Краткая характеристика':
                                short_tech_character = row.td.text
                            elif row.th.text == 'Дополнительная характеристика':
                                extra_character = row.td.text
                            elif row.th.text == 'Цена за единицу':
                                one_price = row.td.text
                            elif row.th.text == 'Количество':
                                count = row.td.text
                            elif row.th.text == 'Запланированная сумма':
                                total_amount = row.td.text
                            elif row.th.text == 'Срок поставки ТРУ':
                                plan_time_of_delivery = row.td.text

                        lot_row = [rows_number, id_appear, id_lot, id_plan, subject_type, tru_code, tru_name, extra_character,
                                              short_tech_character, count, one_price, total_amount, one_price_without_NDS,
                                              amount_without_NDS, amount_without_NDS_to_delivery, start_date, end_date,
                                              plan_time_of_delivery, buying_method, lot_status, fact_amount,
                                              economy, amount_of_delivery_payment]
                        file_writer.writerow(lot_row)
                else:
                    for lot in lots_body[1:]:
                        id_lot = ''
                        id_plan = ''

                        tru_code = ''
                        tru_name = ''
                        extra_character = ''
                        short_tech_character = ''
                        count = ''
                        one_price = ''
                        total_amount = ''
                        one_price_without_NDS = ''
                        amount_without_NDS = ''
                        amount_without_NDS_to_delivery = ''

                        plan_time_of_delivery = ''
                        lot_status = ''
                        fact_amount = ''
                        economy = ''
                        amount_of_delivery_payment = ''

                        rows_number += 1
                        print('rows_number = ' + str(rows_number))
                        nid_lot = lot.a.get('data-lot-id')
                        temp_lot_row = lot.find_all('td')
                        lot_status = temp_lot_row[-2].text
                        id_plan = temp_lot_row[1].text.strip()
                        # print(lot_status)
                        # response = requests.get(url_base + columns[1].a['href'] + lots_url + lot_url, verify=False)
                        # lot_html = response.text
                        # lot_soup = BeautifulSoup(lot_html, 'html.parser')
                        # lot_body = lot_soup.find('div', 'modal-lot-content').table.find_all('tr')
                        # print(lot_body)
                        try:
                            time.sleep(1)
                            driver.get(url_base + columns[1].a['href'] + lots_url)
                            driver.find_element_by_xpath(f"//a[@data-lot-id='{nid_lot}']").click()
                            wait = WebDriverWait(driver, timeout=5)
                        except:
                            pass
                        # print(driver.page_source)
                        lot_soup = BeautifulSoup(driver.page_source, 'html.parser')
                        lot_body = lot_soup.find('div', 'modal-lot-content').table.find_all('tr')
                        for row in lot_body:
                            # if row.th.text == 'Дата начала приема заявок':
                            #     start_date = row.td.text
                            # elif row.th.text == 'Дата окончания приема заявок':
                            #     end_date = row.td.text
                            if row.th.text == 'Код ТРУ':
                                tru_code = row.td.text
                            elif row.th.text == 'Лот №':
                                id_lot = row.td.text
                            elif row.th.text == 'Наименование ТРУ':
                                tru_name = row.td.text
                            elif row.th.text == 'Краткая характеристика':
                                short_tech_character = row.td.text
                            elif row.th.text == 'Дополнительная характеристика':
                                extra_character = row.td.text
                            elif row.th.text == 'Цена за единицу':
                                one_price = row.td.text
                            elif row.th.text == 'Количество':
                                count = row.td.text
                            elif row.th.text == 'Запланированная сумма':
                                total_amount = row.td.text
                            elif row.th.text == 'Срок поставки ТРУ':
                                plan_time_of_delivery = row.td.text

                        lot_row = [rows_number, id_appear, id_lot, id_plan, subject_type, tru_code, tru_name, extra_character,
                                              short_tech_character, count, one_price, total_amount, one_price_without_NDS,
                                              amount_without_NDS, amount_without_NDS_to_delivery, start_date, end_date,
                                              plan_time_of_delivery, buying_method, lot_status, fact_amount,
                                              economy, amount_of_delivery_payment]
                        file_writer.writerow(lot_row)


                # time.sleep(1)
                # response = requests.get(columns[2].a['href'], verify=False)
                # lot_html = response.text
                # lot_soup = BeautifulSoup(lot_html, 'html.parser')
                #
                # lot_rows = lot_soup.table.find_all('tr')
                # for row in lot_rows:
                #     if row.th.text == 'Дата начала приема заявок':
                #         start_date = row.td.text
                #     elif row.th.text == 'Дата окончания приема заявок':
                #         end_date = row.td.text
                #     elif row.th.text == 'Код ТРУ':
                #         tru_code = row.td.text
                #     elif row.th.text == 'Наименование ТРУ':
                #         tru_name = row.td.text
                #     elif row.th.text == 'Краткая характеристика':
                #         short_tech_character = row.td.text
                #     elif row.th.text == 'Дополнительная характеристика':
                #         extra_character = row.td.text
                #     elif row.th.text == 'Цена за единицу':
                #         one_price = row.td.text
                #     elif row.th.text == 'Количество':
                #         count = row.td.text
                #     elif row.th.text == 'Запланированная сумма':
                #         total_amount = row.td.text
                #     elif row.th.text == 'Срок поставки ТРУ':
                #         plan_time_of_delivery = row.td.text
                #
                # lot_row = [rows_number, id_appear, id_lot, id_plan, subject_type, tru_code, tru_name, extra_character,
                #                       short_tech_character, count, one_price, total_amount, one_price_without_NDS,
                #                       amount_without_NDS, amount_without_NDS_to_delivery, start_date, end_date,
                #                       plan_time_of_delivery, buying_method, lot_status, fact_amount,
                #                       economy, amount_of_delivery_payment]
                # file_writer.writerow(lot_row)


# with open("classmates.csv", mode="w", encoding='utf-8') as w_file:
#     # names = ["Имя", "Возраст"]
#     file_writer = csv.writer(w_file, delimiter = ";",
#                                  lineterminator="\r")
#     # file_writer.writeheader()
#     file_writer.writerow(["№", 'id объявления', 'id лота', 'Вид предмета закупок',
#                           'Код товара, работы, услуги (в соответствии с КТРУ)',
#                           'Наименование закупаемых товаров, работ, услуг на государственном языке (в соответствии с КТРУ)',
#                           'Дополнительная характеристика', 'Краткая техническая характеристика', 'Количество, объём',
#                           'Цена за единицу, тенге', 'Сумма, утвержденная  для закупки, тенге',
#                           'Цена (без НДС) по договору, тенге',
#                           'Сумма  (без НДС), договору тенге', 'Сумма (без НДС), оплачен поставщику тенге',
#                           'Дата начала приема заявок', 'Дата окончания приема заявок',
#                           'Планируемый срок осуществления поставки',
#                           'Способ закупки', 'Статус лота',
#                           'Сумма по договору факт', 'Экономия', 'Сумма оплаты поставщику'
#                           ])
#     file_writer.writerow([i for i in range(1,22)])
#     # file_writer.writerow({"Имя": "Вова", "Возраст": "14"})