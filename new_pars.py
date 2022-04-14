import requests


import csv
import time

URL = "https://ows.goszakup.gov.kz/v3/lots"
announce_URL = "https://ows.goszakup.gov.kz/v3/trd-buy/"
CONTRACT_URL = "https://ows.goszakup.gov.kz/v3/contract/"
subject_type = "https://ows.goszakup.gov.kz/v3/refs/ref_subject_type"
plans_URL = "https://ows.goszakup.gov.kz/v3/plans/all"
PLAN_URL = "https://ows.goszakup.gov.kz/v3/plans/view/"
bin_URL = "https://ows.goszakup.gov.kz/v3/subject/biin/"
LOTS_URL = "https://ows.goszakup.gov.kz/v3/lots/number-anno/"

headers = dict()
headers["Authorization"] = "Bearer 3eaae6dd49f1ab32c1421c9db58a3a59"
headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Safari/605.1.15"
headers["Content-Type"] = "application/json"

contract_page_cnt = 1

try:
    r = requests.get(
        CONTRACT_URL,
        headers=headers,
        params={'limit': 500, },
        verify=False
    )
    print(r)
    if r.status_code == 200:
        data = r.json()
        if data.get('total') % data.get('limit') == 0:
            contract_page_cnt = data.get('total') // data.get('limit')
        else:
            contract_page_cnt = data.get('total') // data.get('limit') + 1
        print(data)
        print('contract page count: ', contract_page_cnt)

    year_2022 = True

    with open(f"contracts.csv", mode="w", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=";",
                                 lineterminator="\r")
        file_writer.writerow(['ID договора', 'ID Объявления', 'Номер объявления', 'Статус', 'ИД Поставщика',
                              'БИН/ИИН Поставщика', 'Наименование подтверждающего документа',
                              'Дата подтверждающего документа', 'Дата подведения итогов госзакупок',
                              'ИД заказчика ТРУ', 'БИН заказчика ТРУ', 'Номер договора в системе',
                              'Финансовый год', 'Форма заключения договора', 'Тип закупки (Тип закупки)',
                              'Код валюты договора', 'Сумма заключенного договора без НДС',
                              'Сумма заключенного договора с НДС', 'Дата заключения договора',
                              'Общая фактическая сумма договора', 'Тип договора', 'Описание на казахском языке',
                              'Описание на русском языке', 'Фактический способ закупки', 'Юридический адрес заказчика',
                              'Номер лота', 'Наименование на русском языке', 'Наименование на государственном языке',
                              'Детальное описание на русском языке', 'Детальное описание на государственном языке',
                              'БИН заказчика', 'ИД Способа закупки', 'ИД пункта плана', 'Номер акта',
                              'Код способа закупки(плановый)', 'Код единицы измерения', 'Количество / объем',
                              'Цена за единицу', 'Общая сумма, утвержденная для закупки',
                              'Краткая характеристика на русском языке', 'Краткая характеристика на казахском языке',
                              'Дополнительное описание на русском языке', 'Дополнительное описание на казахском языке',
                              'ID КАТО', 'Полный адрес поставки на русском языке',
                              'Полный адрес поставки на казахском языке',
                              ])

        for x in range(1, contract_page_cnt+1):
            if year_2022:
                while True:
                    try:
                        params = {'limit': 500, 'page' : x}
                        r = requests.get(url=CONTRACT_URL, params=params, headers=headers, verify=False)

                        data = r.json()
                        data = data['items']
                        for contract in data:
                            if year_2022:
                                while True:
                                    try:
                                        contract_detail_response = requests.get(CONTRACT_URL+str(contract.get('id')), headers=headers, verify=False,)
                                        contract_detail_data = contract_detail_response.json()
                                        if contract_detail_data.get('fin_year') == 2022:
                                            while True:
                                                try:
                                                    if contract_detail_data.get('trd_buy_number_anno'):
                                                        lots_response = requests.get(LOTS_URL+contract_detail_data.get('trd_buy_number_anno'), params={'limit': 500, }, headers=headers, verify=False,)
                                                        lots_data = lots_response.json()
                                                        if lots_data.get('total') % lots_data.get('limit') == 0:
                                                            lots_page_cnt = lots_data.get('total') // lots_data.get('limit')
                                                        else:
                                                            lots_page_cnt = lots_data.get('total') // lots_data.get(
                                                                'limit') + 1

                                                        for lots_page in range(1, lots_page_cnt):
                                                            while True:
                                                                try:
                                                                    lots_response = requests.get(
                                                                        LOTS_URL + contract_detail_data.get('trd_buy_number_anno'),
                                                                        params={'limit': 500, 'page': lots_page}, headers=headers, verify=False, )
                                                                    lots_data = lots_response.json()
                                                                    for lot_data in lots_data.get('items'):
                                                                        for plan_point in lot_data.get('point_list'):
                                                                            while True:
                                                                                try:
                                                                                    plan_point_response = requests.get(
                                                                                        PLAN_URL + plan_point, headers=headers,
                                                                                        verify=False, )
                                                                                    plan_point_data = plan_point_response.json()
                                                                                    for kato in plan_point_data.get('kato'):
                                                                                        if kato.get('ref_kato_code')[:2] in ("71", "75") or kato.get('ref_kato_code')[
                                                                                                                                         :4] == "1170":
                                                                                            file_writer.writerow(
                                                                                                [contract_detail_data.get('id'), contract_detail_data.get('trd_buy_id'),
                                                                                                 contract_detail_data.get('trd_buy_number_anno'),
                                                                                                 contract_detail_data.get('ref_contract_status_id'),
                                                                                                 contract_detail_data.get('supplier_id'),
                                                                                                 contract_detail_data.get('supplier_biin'),
                                                                                                 contract_detail_data.get('sign_reason_doc_name'),
                                                                                                 contract_detail_data.get('sign_reason_doc_date'),
                                                                                                 contract_detail_data.get('trd_buy_itogi_date_public'),
                                                                                                 contract_detail_data.get('customer_id'),
                                                                                                 contract_detail_data.get('customer_bin'),
                                                                                                 contract_detail_data.get('contract_number_sys'),
                                                                                                 contract_detail_data.get('fin_year'),
                                                                                                 contract_detail_data.get('ref_contract_agr_form_id'),
                                                                                                 contract_detail_data.get('ref_currency_code'),
                                                                                                 contract_detail_data.get('contract_sum'),
                                                                                                 contract_detail_data.get('contract_sum_wnds'),
                                                                                                 contract_detail_data.get('sign_date'),
                                                                                                 contract_detail_data.get('fakt_sum_wnds'),
                                                                                                 contract_detail_data.get('ref_contract_type_id'),
                                                                                                 contract_detail_data.get('description_kz'),
                                                                                                 contract_detail_data.get('description_ru'),
                                                                                                 contract_detail_data.get('fakt_trade_methods_id'),
                                                                                                 contract_detail_data.get('customer_legal_address'),
                                                                                                 lot_data.get('lot_number'), lot_data.get('name_ru'),
                                                                                                 lot_data.get('name_kz'), lot_data.get('description_ru'),
                                                                                                 lot_data.get('description_kz'),
                                                                                                 lot_data.get('customer_bin'),
                                                                                                 lot_data.get('ref_trade_methods_id'),
                                                                                                 plan_point_data.get('id'),
                                                                                                 plan_point_data.get('plan_act_number'),
                                                                                                 plan_point_data.get('ref_trade_methods_id'),
                                                                                                 plan_point_data.get('ref_units_code'),
                                                                                                 plan_point_data.get('count'),
                                                                                                 plan_point_data.get('price'),
                                                                                                 plan_point_data.get('amount'),
                                                                                                 plan_point_data.get('desc_ru'),
                                                                                                 plan_point_data.get('desc_kz'),
                                                                                                 plan_point_data.get('extra_desc_ru'),
                                                                                                 plan_point_data.get('extra_desc_kz'),
                                                                                                 kato.get('ref_kato_code'),
                                                                                                 kato.get('full_delivery_place_name_ru'),
                                                                                                 kato.get('full_delivery_place_name_kz'),

                                                                                                 ])
                                                                                    break
                                                                                except:
                                                                                    time.sleep(5)
                                                                                    print('plan_point_response: error')
                                                                                    print('page: ', x)
                                                                                    print('contract detail id: ', contract_detail_data.get('id'))
                                                                                    print('contract detail number anno: ', contract_detail_data.get('trd_buy_number_anno'))
                                                                                    print('lot number: ', lot_data.get('lot_number'))
                                                                                    print('plan point id: ', plan_point_data.get('id'))
                                                                    break
                                                                except:
                                                                    time.sleep(5)
                                                                    print('lots_data_response: error')
                                                                    print('page: ', x)
                                                                    print('contract detail id: ',
                                                                          contract_detail_data.get('id'))
                                                                    print('contract detail number anno: ',
                                                                          contract_detail_data.get('trd_buy_number_anno'))
                                                                    print('lots page: ', lots_page)
                                                    else:
                                                        break
                                                    break
                                                except:
                                                    time.sleep(5)
                                                    print('lots_data_response: error')
                                                    print('page: ', x)
                                                    print('contract detail id: ',
                                                          contract_detail_data.get('id'))
                                                    print('contract detail number anno: ',
                                                          contract_detail_data.get('trd_buy_number_anno'))
                                                    print('lots page: ', lots_page)
                                        else:
                                            print('Год 2022 закончился')
                                            print('page: ', x)
                                            print('contract detail id: ',
                                                  contract_detail_data.get('id'))
                                            print('contract detail number anno: ',
                                                  contract_detail_data.get('trd_buy_number_anno'))
                                            year_2022 = False
                                            break
                                        break
                                    except:
                                        time.sleep(5)
                                        print('contract_detail_response: error')
                                        print('page: ', x)
                                        print('contract detail id: ', contract_detail_data.get('id'))
                                        print('contract detail number anno: ',
                                              contract_detail_data.get('trd_buy_number_anno'))
                            else:
                                break
                        break
                    except:
                        time.sleep(5)
                        print('contracts_response: error')
                        print('page: ', x)
            else:
                break
except Exception as err:
    print(err)