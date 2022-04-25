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
TRADE_METHODS_URL = "https://ows.goszakup.gov.kz/v3/refs/ref_trade_methods"
UNITS_CODE_URL = "https://ows.goszakup.gov.kz/v3/refs/ref_units"

headers = dict()
headers["Authorization"] = "Bearer dbc38bf745fd37a65e012c7f58e5bbdd"
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


response = requests.get(TRADE_METHODS_URL, headers=headers, verify=False, params={'limit': 500, })
data = response.json()
TRADE_METHODS_CODES = dict()
for i in data.get('items'):
    TRADE_METHODS_CODES[i.get('id')] = i.get('name_ru')

response = requests.get(UNITS_CODE_URL, headers=headers, verify=False, params={'limit': 500, })
data = response.json()
UNITS_CODES = dict()
for i in data.get('items'):
    UNITS_CODES[i.get('code')] = i.get('name_ru')


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
                "after": 14450271,
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

    contract_page_cnt = 270

    print('contract page count: ', contract_page_cnt)

    with open(f"contracts_6.csv", mode="w", encoding='utf-8') as w_file:
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
                              'ИД пункта плана', 'Номер акта',
                              'Способа закупки(плановый)', 'Единицы измерения', 'Количество / объем',
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

                            for lots_page in range(1, lots_page_cnt+1):
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
                                                            PLAN_URL + str(plan_point), headers=headers,
                                                            verify=False, )
                                                        plan_point_data = plan_point_response.json()
                                                        if plan_point_data.get(
                                                                'ref_pln_point_status_id') == 9 and plan_point_data.get('kato'):
                                                            for kato in plan_point_data.get('kato'):
                                                                if kato.get('ref_kato_code')[:2] in (
                                                                        "71", "75") or kato.get('ref_kato_code')[
                                                                                       :4] == "1170":
                                                                    if contract.get(
                                                                             'signReasonDocName'):
                                                                        signReasonName = contract.get(
                                                                             'signReasonDocName').strip()
                                                                    else:
                                                                        signReasonName = contract.get(
                                                                             'signReasonDocName')

                                                                    if contract.get(
                                                                             'descriptionKz'):
                                                                        desc_kz1 = contract.get(
                                                                             'descriptionKz').strip()
                                                                    else:
                                                                        desc_kz1 = contract.get(
                                                                             'descriptionKz')

                                                                    if contract.get(
                                                                             'descriptionRu'):
                                                                        desc_ru1 = contract.get(
                                                                             'descriptionRu').strip()
                                                                    else:
                                                                        desc_ru1 = contract.get(
                                                                             'descriptionRu')

                                                                    if contract.get(
                                                                             'customerLegalAddress'):
                                                                        customer_addr = contract.get(
                                                                             'customerLegalAddress').strip()
                                                                    else:
                                                                        customer_addr = contract.get(
                                                                             'customerLegalAddress')

                                                                    if lot_data.get('name_ru'):
                                                                        lot_name_ru = lot_data.get('name_ru').strip()
                                                                    else:
                                                                        lot_name_ru = lot_data.get('name_ru')

                                                                    if lot_data.get('name_kz'):
                                                                        lot_name_kz = lot_data.get('name_kz').strip()
                                                                    else:
                                                                        lot_name_kz = lot_data.get('name_kz')

                                                                    if lot_data.get('description_ru'):
                                                                        lot_desc_ru = lot_data.get('description_ru').strip()
                                                                    else:
                                                                        lot_desc_ru = lot_data.get('description_ru')

                                                                    if lot_data.get('description_kz'):
                                                                        lot_desc_kz = lot_data.get('description_kz').strip()
                                                                    else:
                                                                        lot_desc_kz = lot_data.get('description_kz')

                                                                    if plan_point_data.get('desc_ru'):
                                                                        desc_ru2 = plan_point_data.get('desc_ru').strip()
                                                                    else:
                                                                        desc_ru2 = plan_point_data.get('desc_ru')

                                                                    if plan_point_data.get('desc_kz'):
                                                                        desc_kz2 = plan_point_data.get('desc_kz').strip()
                                                                    else:
                                                                        desc_kz2 = plan_point_data.get('desc_kz')

                                                                    if plan_point_data.get(
                                                                             'extra_desc_ru'):
                                                                        extra_desc_ru2 = plan_point_data.get(
                                                                             'extra_desc_ru').strip()
                                                                    else:
                                                                        extra_desc_ru2 = plan_point_data.get(
                                                                             'extra_desc_ru')

                                                                    if plan_point_data.get(
                                                                             'extra_desc_kz'):
                                                                        extra_desc_kz2 = plan_point_data.get(
                                                                             'extra_desc_kz').strip()
                                                                    else:
                                                                        extra_desc_kz2 = plan_point_data.get(
                                                                             'extra_desc_ru')

                                                                    if kato.get(
                                                                             'full_delivery_place_name_ru'):
                                                                        kato_ru = kato.get(
                                                                             'full_delivery_place_name_ru').strip()
                                                                    else:
                                                                        kato_ru = kato.get(
                                                                             'full_delivery_place_name_ru')

                                                                    if kato.get(
                                                                             'full_delivery_place_name_kz'):
                                                                        kato_kz = kato.get(
                                                                             'full_delivery_place_name_kz').strip()
                                                                    else:
                                                                        kato_kz = kato.get(
                                                                             'full_delivery_place_name_kz')

                                                                    if contract.get(
                                                                            'RefContractYearType'):
                                                                        contract_type = contract.get(
                                                                            'RefContractYearType').get(
                                                                            'nameRu')
                                                                    else:
                                                                        contract_type = contract.get(
                                                                            'RefContractYearType')

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
                                                                         signReasonName,
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
                                                                         contract_type,
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
                                                                         desc_kz1,
                                                                         desc_ru1,
                                                                         customer_addr,
                                                                         lot_data.get('lot_number'),
                                                                         lot_name_ru,
                                                                         lot_name_kz,
                                                                         lot_desc_ru,
                                                                         lot_desc_kz,
                                                                         plan_point_data.get('id'),
                                                                         plan_point_data.get(
                                                                             'plan_act_number'),
                                                                         TRADE_METHODS_CODES.get(plan_point_data.get(
                                                                             'ref_trade_methods_id')),
                                                                         UNITS_CODES.get(plan_point_data.get(
                                                                             'ref_units_code')),
                                                                         plan_point_data.get('count'),
                                                                         plan_point_data.get('price'),
                                                                         plan_point_data.get('amount'),
                                                                         desc_ru2,
                                                                         desc_kz2,
                                                                         extra_desc_ru2,
                                                                         extra_desc_kz2,
                                                                         kato.get('ref_kato_code'),
                                                                         kato_ru,
                                                                         kato_kz,

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
                                                        print('plan point id: ', plan_point)
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

                                        for lots_page in range(1, lots_page_cnt + 1):
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
                                                                        PLAN_URL + str(plan_point), headers=headers,
                                                                        verify=False, )
                                                                    plan_point_data = plan_point_response.json()
                                                                    if plan_point_data.get(
                                                                            'ref_pln_point_status_id') == 9 and plan_point_data.get(
                                                                        'kato'):
                                                                        for kato in plan_point_data.get('kato'):
                                                                            if kato.get('ref_kato_code')[:2] in (
                                                                                    "71", "75") or kato.get(
                                                                                'ref_kato_code')[
                                                                                                   :4] == "1170":
                                                                                if contract.get(
                                                                                        'signReasonDocName'):
                                                                                    signReasonName = contract.get(
                                                                                        'signReasonDocName').strip()
                                                                                else:
                                                                                    signReasonName = contract.get(
                                                                                        'signReasonDocName')

                                                                                if contract.get(
                                                                                        'descriptionKz'):
                                                                                    desc_kz1 = contract.get(
                                                                                        'descriptionKz').strip()
                                                                                else:
                                                                                    desc_kz1 = contract.get(
                                                                                        'descriptionKz')

                                                                                if contract.get(
                                                                                        'descriptionRu'):
                                                                                    desc_ru1 = contract.get(
                                                                                        'descriptionRu').strip()
                                                                                else:
                                                                                    desc_ru1 = contract.get(
                                                                                        'descriptionRu')

                                                                                if contract.get(
                                                                                        'customerLegalAddress'):
                                                                                    customer_addr = contract.get(
                                                                                        'customerLegalAddress').strip()
                                                                                else:
                                                                                    customer_addr = contract.get(
                                                                                        'customerLegalAddress')

                                                                                if lot_data.get('name_ru'):
                                                                                    lot_name_ru = lot_data.get(
                                                                                        'name_ru').strip()
                                                                                else:
                                                                                    lot_name_ru = lot_data.get(
                                                                                        'name_ru')

                                                                                if lot_data.get('name_kz'):
                                                                                    lot_name_kz = lot_data.get(
                                                                                        'name_kz').strip()
                                                                                else:
                                                                                    lot_name_kz = lot_data.get(
                                                                                        'name_kz')

                                                                                if lot_data.get('description_ru'):
                                                                                    lot_desc_ru = lot_data.get(
                                                                                        'description_ru').strip()
                                                                                else:
                                                                                    lot_desc_ru = lot_data.get(
                                                                                        'description_ru')

                                                                                if lot_data.get('description_kz'):
                                                                                    lot_desc_kz = lot_data.get(
                                                                                        'description_kz').strip()
                                                                                else:
                                                                                    lot_desc_kz = lot_data.get(
                                                                                        'description_kz')

                                                                                if plan_point_data.get('desc_ru'):
                                                                                    desc_ru2 = plan_point_data.get(
                                                                                        'desc_ru').strip()
                                                                                else:
                                                                                    desc_ru2 = plan_point_data.get(
                                                                                        'desc_ru')

                                                                                if plan_point_data.get('desc_kz'):
                                                                                    desc_kz2 = plan_point_data.get(
                                                                                        'desc_kz').strip()
                                                                                else:
                                                                                    desc_kz2 = plan_point_data.get(
                                                                                        'desc_kz')

                                                                                if plan_point_data.get(
                                                                                        'extra_desc_ru'):
                                                                                    extra_desc_ru2 = plan_point_data.get(
                                                                                        'extra_desc_ru').strip()
                                                                                else:
                                                                                    extra_desc_ru2 = plan_point_data.get(
                                                                                        'extra_desc_ru')

                                                                                if plan_point_data.get(
                                                                                        'extra_desc_kz'):
                                                                                    extra_desc_kz2 = plan_point_data.get(
                                                                                        'extra_desc_kz').strip()
                                                                                else:
                                                                                    extra_desc_kz2 = plan_point_data.get(
                                                                                        'extra_desc_ru')

                                                                                if kato.get(
                                                                                        'full_delivery_place_name_ru'):
                                                                                    kato_ru = kato.get(
                                                                                        'full_delivery_place_name_ru').strip()
                                                                                else:
                                                                                    kato_ru = kato.get(
                                                                                        'full_delivery_place_name_ru')

                                                                                if kato.get(
                                                                                        'full_delivery_place_name_kz'):
                                                                                    kato_kz = kato.get(
                                                                                        'full_delivery_place_name_kz').strip()
                                                                                else:
                                                                                    kato_kz = kato.get(
                                                                                        'full_delivery_place_name_kz')

                                                                                if contract.get(
                                                                                         'RefContractYearType'):
                                                                                    contract_type = contract.get(
                                                                                         'RefContractYearType').get(
                                                                                         'nameRu')
                                                                                else:
                                                                                    contract_type = contract.get(
                                                                                         'RefContractYearType')

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
                                                                                     signReasonName,
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
                                                                                     contract_type,
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
                                                                                     desc_kz1,
                                                                                     desc_ru1,
                                                                                     customer_addr,
                                                                                     lot_data.get('lot_number'),
                                                                                     lot_name_ru,
                                                                                     lot_name_kz,
                                                                                     lot_desc_ru,
                                                                                     lot_desc_kz,
                                                                                     plan_point_data.get('id'),
                                                                                     plan_point_data.get(
                                                                                         'plan_act_number'),
                                                                                     TRADE_METHODS_CODES.get(
                                                                                         plan_point_data.get(
                                                                                             'ref_trade_methods_id')),
                                                                                     UNITS_CODES.get(
                                                                                         plan_point_data.get(
                                                                                             'ref_units_code')),
                                                                                     plan_point_data.get('count'),
                                                                                     plan_point_data.get('price'),
                                                                                     plan_point_data.get('amount'),
                                                                                     desc_ru2,
                                                                                     desc_kz2,
                                                                                     extra_desc_ru2,
                                                                                     extra_desc_kz2,
                                                                                     kato.get('ref_kato_code'),
                                                                                     kato_ru,
                                                                                     kato_kz,

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
                                                                    print('plan point id: ', plan_point)
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
                                    print(err)

                    break
                except Exception as err:
                    time.sleep(5)
                    print('contracts_response: error')
                    print('page: ', x)
                    print(err)
except Exception as err:
    print(err)