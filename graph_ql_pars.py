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
headers[
    "User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Safari/605.1.15"
headers["Content-Type"] = "application/json"

contract_page_cnt = 1

trade_methods = {
    2: 'Открытый конкурс',
    3: 'Запрос ценовых предложений',
    32: 'Конкурс с предварительным квалификационным отбором',
    60: 'Электронный магазин',
}

exclude_bin = {
    '900640000128',
    '970940001378',
    '050840004139',
    '000740001307',
    '990740002243',
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
    '120940001946',
    '780140000023',
    '990340005977',
    '171041003124',
    '960640000535',
    '940940000384',
    '210240019348',
    '980440001034',
    '030440003698',
    '180740010700',
}

# try:
#     r = requests.post(
#         "https://ows.goszakup.gov.kz/v3/graphql",
#         json={
#             "query": '''
#                 query($limit: Int, $after: Int, $filter: ContractFiltersInput){
#                     Contract(limit: $limit, after: $after, filter: $filter) {
#                         id
#                         trdBuyId
#                         trdBuyNumberAnno
#
#                         FaktTradeMethods {
#                             id
#                             nameRu
#                         }
#                         supplierBiin
#                         signReasonDocName
#                         signReasonDocDate
#                         trdBuyItogiDatePublic
#                         customerId
#                         customerBin
#                         contractNumberSys
#                         finYear
#                         refContractAgrFormId
#                         refCurrencyCode
#                         contractSum
#                         contractSumWnds
#                         signDate
#                         faktSumWnds
#                         refContractTypeId
#                         descriptionKz
#                         descriptionRu
#                         customerLegalAddress
#
#                     }
#                 }
#             ''',
#             "variables": {
#                 "limit": 10,
#                 #                 "after": 7413101,
#                 "filter": {
#                     #                     "id": [7413101,7413083],
#                     "finYear": 2022,
#                     #                     "customerBin": '900640000128',
#                     #                     "or": {
#                     #                         "customerBin": '970940001378'
#                     #                     }
#                     # "or": [
#                     #     {"or": [{customerBin: {eq: "900640000128"}}]},
#                     #     {"or": [{customerBin: {eq: "970940001378"}}]}
#                     # ]
#                     "faktTradeMethodsId": list(trade_methods.keys()),
#                     #                     "customerBin": {ne: "Unwanted"} {
#                     #                         exclude_bin,
#                     #                     }
#                     #                     "not": {
#                     #                         "customerBin": {
#                     #                             '900640000128'
#                     #                         }
#                     #                     }
#                     #                     "customerBin": '900640000128',
#                 }
#             },
#         },
#         headers=headers,
#         verify=False,
#     )
#
#     data = r.json()
#     if data.get('extensions').get('pageInfo').get('totalCount') % data.get('extensions').get('pageInfo').get('limitPage') == 0:
#         contract_page_cnt = data.get('extensions').get('pageInfo').get('totalCount') // data.get('extensions').get('pageInfo').get('limitPage')
#     else:
#         contract_page_cnt = data.get('extensions').get('pageInfo').get('totalCount') // data.get('extensions').get('pageInfo').get('limitPage') + 1
#
#     print(data)
#     print('contract page count: ', contract_page_cnt)
#
# except:
#     pass


# year_2022 = True
#
# for x in range(1, contract_page_cnt+1):
#     if year_2022:
#         params = {'limit': 500, 'page' : x}
#         r = requests.get(url=CONTRACT_URL, params=params, headers=headers, verify=False)
#         data = r.json()
#         data = data['items']
#         for contract in data:
#             if year_2022:
#                 contract_detail_response = requests.get(
#                     CONTRACT_URL+str(contract.get('id')),
#                     params={
#                         'fin_year': 2022,
#                     },
#                     headers=headers,
#                     verify=False,
#                 )
#                 contract_detail_data = contract_detail_response.json()
#                 if contract_detail_data.get('fin_year') != 2022:
#                     print('no 2022')


# # try:
# #     r = requests.get(
# #         "https://ows.goszakup.gov.kz/v3/refs/ref_pln_point_status",
# #         headers=headers,
# #         params={'limit': 500, },
# #         verify=False
# #     )
# #     print(r.json())
# #     for i in r.json().get('items'):
# #         print(i)
# # except:
# #     pass

try:
    r = requests.post(
        "https://ows.goszakup.gov.kz/v3/graphql",
        json={
            "query": '''
                query($limit: Int, $after: Int, $filter: ContractFiltersInput){
                    Contract(limit: $limit, after: $after, filter: $filter) {
                        id
                        trdBuyId
                        trdBuyNumberAnno

                        FaktTradeMethods {
                            id
                            nameRu
                        }
                        supplierId
                        supplierBiin
                        signReasonDocName
                        signReasonDocDate
                        trdBuyItogiDatePublic
                        customerId
                        customerBin
                        contractNumberSys
                        finYear
                        refContractAgrFormId
                        RefContractYearType {
                            id
                            nameRu
                        }
                        refCurrencyCode
                        contractSum
                        contractSumWnds
                        signDate
                        faktSumWnds
                        refContractTypeId
                        descriptionKz
                        descriptionRu
                        customerLegalAddress

                    }
                }
            ''',
            "variables": {
                "limit": 200,
                "filter": {
                    "finYear": 2022,
                    "faktTradeMethodsId": list(trade_methods.keys()),
                }
            },
        },
        headers=headers,
        verify=False,
    )

    data = r.json()
    print(data)

    if data.get('extensions').get('pageInfo').get('totalCount') % data.get('extensions').get('pageInfo').get(
            'limitPage') == 0:
        contract_page_cnt = data.get('extensions').get('pageInfo').get('totalCount') // data.get('extensions').get(
            'pageInfo').get('limitPage')
    else:
        contract_page_cnt = data.get('extensions').get('pageInfo').get('totalCount') // data.get('extensions').get(
            'pageInfo').get('limitPage') + 1

    print('contract page count: ', contract_page_cnt)

    with open(f"contracts.csv", mode="w", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=";",
                                 lineterminator="\r")
        file_writer.writerow(['ID договора', 'ID Объявления', 'Номер объявления', 'Статус плана',
                              'Способ закупки', 'ИД Поставщика',
                              'БИН/ИИН Поставщика', 'Наименование подтверждающего документа',
                              'Дата подтверждающего документа', 'Дата подведения итогов госзакупок',
                              'ИД заказчика ТРУ', 'БИН заказчика ТРУ', 'Номер договора в системе',
                              'Финансовый год', 'Форма заключения договора', 'Тип закупки',
                              'Код валюты договора', 'Сумма заключенного договора без НДС',
                              'Сумма заключенного договора с НДС', 'Дата заключения договора',
                              'Общая фактическая сумма договора', 'Тип договора', 'Описание на казахском языке',
                              'Описание на русском языке', 'Юридический адрес заказчика',
                              'Номер лота', 'Наименование на русском языке', 'Наименование на государственном языке',
                              'Детальное описание на русском языке', 'Детальное описание на государственном языке',
                              'БИН заказчика', 'ИД пункта плана', 'Номер акта',
                              'Код способа закупки(плановый)', 'Код единицы измерения', 'Количество / объем',
                              'Цена за единицу', 'Общая сумма, утвержденная для закупки',
                              'Краткая характеристика на русском языке', 'Краткая характеристика на казахском языке',
                              'Дополнительное описание на русском языке', 'Дополнительное описание на казахском языке',
                              'ID КАТО', 'Полный адрес поставки на русском языке',
                              'Полный адрес поставки на казахском языке',
                              ])

        for contract in data.get('data').get('Contract'):
            if contract.get('customerBin') not in exclude_bin:
                while True:
                    try:
                        if contract.get('trdBuyNumberAnno'):
                            lots_response = requests.get(
                                LOTS_URL + contract.get('trdBuyNumberAnno'),
                                params={'limit': 500, }, headers=headers, verify=False, )
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
                                            LOTS_URL + contract.get('trdBuyNumberAnno'),
                                            params={'limit': 500, 'page': lots_page}, headers=headers,
                                            verify=False, )
                                        lots_data = lots_response.json()
                                        for lot_data in lots_data.get('items'):
                                            for plan_point in lot_data.get('point_list'):
                                                while True:
                                                    try:
                                                        plan_point_response = requests.get(
                                                            PLAN_URL + plan_point, headers=headers,
                                                            verify=False, )
                                                        plan_point_data = plan_point_response.json()
                                                        if plan_point_data.get(
                                                                'ref_pln_point_status_id') == 9:
                                                            for kato in plan_point_data.get('kato'):
                                                                if kato.get('ref_kato_code')[:2] in (
                                                                        "71", "75") or kato.get('ref_kato_code')[
                                                                                       :4] == "1170":
                                                                    file_writer.writerow(
                                                                        [contract.get('id'),
                                                                         contract.get(
                                                                             'trdBuyId'),
                                                                         contract.get(
                                                                             'trdBuyNumberAnno'),
                                                                         'Закупка состоялась',
                                                                         trade_methods.get(
                                                                             contract.get(
                                                                                 'FaktTradeMethods').get('id')),
                                                                         contract.get(
                                                                             'supplierId'),
                                                                         contract.get(
                                                                             'supplierBiin'),
                                                                         contract.get(
                                                                             'signReasonDocName'),
                                                                         contract.get(
                                                                             'signReasonDocDate'),
                                                                         contract.get(
                                                                             'trdBuyItogiDatePublic'),
                                                                         contract.get(
                                                                             'customerId'),
                                                                         contract.get(
                                                                             'customerBin'),
                                                                         contract.get(
                                                                             'contractNumberSys'),
                                                                         contract.get(
                                                                             'finYear'),
                                                                         contract.get(
                                                                             'refContractAgrFormId'),
                                                                         contract.get(
                                                                             'RefContractYearType').get('nameRu'),
                                                                         contract.get(
                                                                             'refCurrencyCode'),
                                                                         contract.get(
                                                                             'contractSum'),
                                                                         contract.get(
                                                                             'contractSumWnds'),
                                                                         contract.get(
                                                                             'signDate'),
                                                                         contract.get(
                                                                             'faktSumWnds'),
                                                                         contract.get(
                                                                             'refContractTypeId'),
                                                                         contract.get(
                                                                             'descriptionKz'),
                                                                         contract.get(
                                                                             'descriptionRu'),
                                                                         contract.get(
                                                                             'customerLegalAddress'),
                                                                         lot_data.get('lot_number'),
                                                                         lot_data.get('name_ru'),
                                                                         lot_data.get('name_kz'),
                                                                         lot_data.get('description_ru'),
                                                                         lot_data.get('description_kz'),
                                                                         lot_data.get('customer_bin'),
                                                                         plan_point_data.get('id'),
                                                                         plan_point_data.get(
                                                                             'plan_act_number'),
                                                                         plan_point_data.get(
                                                                             'ref_trade_methods_id'),
                                                                         plan_point_data.get(
                                                                             'ref_units_code'),
                                                                         plan_point_data.get('count'),
                                                                         plan_point_data.get('price'),
                                                                         plan_point_data.get('amount'),
                                                                         plan_point_data.get('desc_ru'),
                                                                         plan_point_data.get('desc_kz'),
                                                                         plan_point_data.get(
                                                                             'extra_desc_ru'),
                                                                         plan_point_data.get(
                                                                             'extra_desc_kz'),
                                                                         kato.get('ref_kato_code'),
                                                                         kato.get(
                                                                             'full_delivery_place_name_ru'),
                                                                         kato.get(
                                                                             'full_delivery_place_name_kz'),

                                                                         ])
                                                        break
                                                    except Exception as err:
                                                        time.sleep(5)
                                                        print('plan_point_response: error')
                                                        print('page: ', 1)
                                                        print('contract detail id: ',
                                                              contract.get('id'))
                                                        print('contract detail number anno: ',
                                                              contract.get(
                                                                  'trdBuyNumberAnno'))
                                                        print('lot number: ', lot_data.get('lot_number'))
                                                        print('plan point id: ', plan_point_data.get('id'))
                                                        print(err)
                                        break
                                    except Exception as err:
                                        time.sleep(5)
                                        print('lots_data_response: error')
                                        print('page: ', 1)
                                        print('contract detail id: ',
                                              contract.get('id'))
                                        print('contract detail number anno: ',
                                              contract.get('trdBuyNumberAnno'))
                                        print('lots page: ', lots_page)
                                        print(err)
                        break
                    except Exception as err:
                        time.sleep(5)
                        print('lots_data_response: error')
                        print('page: ', 1)
                        print('contract detail id: ',
                              contract.get('id'))
                        print('contract detail number anno: ',
                              contract.get('trdBuyNumberAnno'))
                        print('lots page: ', lots_page)
                        print(err)

        last_id = data.get('extensions').get('pageInfo').get('lastId')

        for x in range(2, contract_page_cnt+1):
            while True:
                try:
                    r = requests.post(
                        "https://ows.goszakup.gov.kz/v3/graphql",
                        json={
                            "query": '''
                                    query($limit: Int, $after: Int, $filter: ContractFiltersInput){
                                        Contract(limit: $limit, after: $after, filter: $filter) {
                                            id
                                            trdBuyId
                                            trdBuyNumberAnno

                                            FaktTradeMethods {
                                                id
                                                nameRu
                                            }
                                            supplierBiin
                                            signReasonDocName
                                            signReasonDocDate
                                            trdBuyItogiDatePublic
                                            customerId
                                            customerBin
                                            contractNumberSys
                                            finYear
                                            refContractAgrFormId
                                            refCurrencyCode
                                            contractSum
                                            contractSumWnds
                                            signDate
                                            faktSumWnds
                                            refContractTypeId
                                            descriptionKz
                                            descriptionRu
                                            customerLegalAddress

                                        }
                                    }
                                ''',
                            "variables": {
                                "limit": 200,
                                "after": last_id,
                                "filter": {
                                    "finYear": 2022,
                                    "faktTradeMethodsId": list(trade_methods.keys()),
                                }
                            },
                        },
                        headers=headers,
                        verify=False,
                    )

                    data = r.json()
                    last_id = data.get('extensions').get('pageInfo').get('lastId')
                    print('Page: ', x)

                    for contract in data.get('data').get('Contract'):
                        if contract.get('customerBin') not in exclude_bin:
                            while True:
                                try:
                                    if contract.get('trdBuyNumberAnno'):
                                        lots_response = requests.get(
                                            LOTS_URL + contract.get('trdBuyNumberAnno'),
                                            params={'limit': 500, }, headers=headers, verify=False, )
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
                                                        LOTS_URL + contract.get('trdBuyNumberAnno'),
                                                        params={'limit': 500, 'page': lots_page}, headers=headers,
                                                        verify=False, )
                                                    lots_data = lots_response.json()
                                                    for lot_data in lots_data.get('items'):
                                                        for plan_point in lot_data.get('point_list'):
                                                            while True:
                                                                try:
                                                                    plan_point_response = requests.get(
                                                                        PLAN_URL + plan_point, headers=headers,
                                                                        verify=False, )
                                                                    plan_point_data = plan_point_response.json()
                                                                    if plan_point_data.get(
                                                                            'ref_pln_point_status_id') == 9:
                                                                        for kato in plan_point_data.get('kato'):
                                                                            if kato.get('ref_kato_code')[:2] in (
                                                                                    "71", "75") or kato.get(
                                                                                'ref_kato_code')[
                                                                                                   :4] == "1170":
                                                                                file_writer.writerow(
                                                                                    [contract.get('id'),
                                                                                     contract.get(
                                                                                         'trdBuyId'),
                                                                                     contract.get(
                                                                                         'trdBuyNumberAnno'),
                                                                                     'Закупка состоялась',
                                                                                     trade_methods.get(
                                                                                         contract.get(
                                                                                             'FaktTradeMethods').get(
                                                                                             'id')),
                                                                                     contract.get(
                                                                                         'supplierId'),
                                                                                     contract.get(
                                                                                         'supplierBiin'),
                                                                                     contract.get(
                                                                                         'signReasonDocName'),
                                                                                     contract.get(
                                                                                         'signReasonDocDate'),
                                                                                     contract.get(
                                                                                         'trdBuyItogiDatePublic'),
                                                                                     contract.get(
                                                                                         'customerId'),
                                                                                     contract.get(
                                                                                         'customerBin'),
                                                                                     contract.get(
                                                                                         'contractNumberSys'),
                                                                                     contract.get(
                                                                                         'finYear'),
                                                                                     contract.get(
                                                                                         'refContractAgrFormId'),
                                                                                     contract.get(
                                                                                         'RefContractYearType').get(
                                                                                         'nameRu'),
                                                                                     contract.get(
                                                                                         'refCurrencyCode'),
                                                                                     contract.get(
                                                                                         'contractSum'),
                                                                                     contract.get(
                                                                                         'contractSumWnds'),
                                                                                     contract.get(
                                                                                         'signDate'),
                                                                                     contract.get(
                                                                                         'faktSumWnds'),
                                                                                     contract.get(
                                                                                         'refContractTypeId'),
                                                                                     contract.get(
                                                                                         'descriptionKz'),
                                                                                     contract.get(
                                                                                         'descriptionRu'),
                                                                                     contract.get(
                                                                                         'customerLegalAddress'),
                                                                                     lot_data.get('lot_number'),
                                                                                     lot_data.get('name_ru'),
                                                                                     lot_data.get('name_kz'),
                                                                                     lot_data.get('description_ru'),
                                                                                     lot_data.get('description_kz'),
                                                                                     lot_data.get('customer_bin'),
                                                                                     plan_point_data.get('id'),
                                                                                     plan_point_data.get(
                                                                                         'plan_act_number'),
                                                                                     plan_point_data.get(
                                                                                         'ref_trade_methods_id'),
                                                                                     plan_point_data.get(
                                                                                         'ref_units_code'),
                                                                                     plan_point_data.get('count'),
                                                                                     plan_point_data.get('price'),
                                                                                     plan_point_data.get('amount'),
                                                                                     plan_point_data.get('desc_ru'),
                                                                                     plan_point_data.get('desc_kz'),
                                                                                     plan_point_data.get(
                                                                                         'extra_desc_ru'),
                                                                                     plan_point_data.get(
                                                                                         'extra_desc_kz'),
                                                                                     kato.get('ref_kato_code'),
                                                                                     kato.get(
                                                                                         'full_delivery_place_name_ru'),
                                                                                     kato.get(
                                                                                         'full_delivery_place_name_kz'),

                                                                                     ])
                                                                    break
                                                                except Exception as err:
                                                                    time.sleep(5)
                                                                    print('plan_point_response: error')
                                                                    print('page: ', x)
                                                                    print('contract detail id: ',
                                                                          contract.get('id'))
                                                                    print('contract detail number anno: ',
                                                                          contract.get(
                                                                              'trdBuyNumberAnno'))
                                                                    print('lot number: ', lot_data.get('lot_number'))
                                                                    print('plan point id: ', plan_point_data.get('id'))
                                                                    print(err)
                                                    break
                                                except Exception as err:
                                                    time.sleep(5)
                                                    print('lots_data_response: error')
                                                    print('page: ', x)
                                                    print('contract detail id: ',
                                                          contract.get('id'))
                                                    print('contract detail number anno: ',
                                                          contract.get('trdBuyNumberAnno'))
                                                    print('lots page: ', lots_page)
                                                    print(err)
                                    break
                                except Exception as err:
                                    time.sleep(5)
                                    print('lots_data_response: error')
                                    print('page: ', x)
                                    print('contract detail id: ',
                                          contract.get('id'))
                                    print('contract detail number anno: ',
                                          contract.get('trdBuyNumberAnno'))
                                    print('lots page: ', lots_page)
                                    print(err)

                    break
                except Exception as err:
                    time.sleep(5)
                    print('contracts_response: error')
                    print('page: ', x)
                    print(err)
except Exception as err:
    print(err)