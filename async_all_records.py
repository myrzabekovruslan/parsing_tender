import requests
import asyncio
import aiohttp
import aiocsv
import aiofiles
import csv
import time
import sys

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
PLAN_STATUS_URL = "https://ows.goszakup.gov.kz/v3/refs/ref_pln_point_status"

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

response = requests.get(PLAN_STATUS_URL, headers=headers, verify=False, params={'limit': 500, })
data = response.json()
PLAN_STATUS = dict()
for i in data.get('items'):
    PLAN_STATUS[i.get('id')] = i.get('name_ru')

async def parser():
    try:
        async with aiohttp.ClientSession() as session:
            r = await session.post(
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
                                ContractUnits {
                                    lotId
                                    Plans {
                                        id
                                        contractPrevPointId
                                        refPlnPointStatusId
                                        refTradeMethodsId
                                        refUnitsCode
                                        count
                                        price
                                        amount
                                        plnPointYear
                                        descRu
                                        descKz
                                        extraDescKz
                                        extraDescRu
                                        PlansKato {
                                            refKatoCode
                                            fullDeliveryPlaceNameRu
                                            fullDeliveryPlaceNameKz
                                        }
                                    }
                                }

                            }
                        }
                    ''',
                    "variables": {
                        "limit": 200,
                        "filter": {
                            "finYear": 2022,
                        }
                    },
                },
                headers=headers,
            )

            data = await r.json()
            print(data)


            if data.get('extensions').get('pageInfo').get('totalCount') % data.get('extensions').get('pageInfo').get(
                    'limitPage') == 0:
                contract_page_cnt = data.get('extensions').get('pageInfo').get('totalCount') // data.get(
                    'extensions').get(
                    'pageInfo').get('limitPage')
            else:
                contract_page_cnt = data.get('extensions').get('pageInfo').get('totalCount') // data.get(
                    'extensions').get(
                    'pageInfo').get('limitPage') + 1

            print('contract page count: ', contract_page_cnt)

            async with aiofiles.open("contracts.csv", mode="w", encoding='utf-8') as w_file:
                file_writer = aiocsv.AsyncWriter(w_file, delimiter=";",
                                                 lineterminator="\r")
                await file_writer.writerow(['ID договора', 'ID Объявления', 'Номер объявления',
                                            'Способ закупки', 'ИД Поставщика',
                                            'БИН/ИИН Поставщика', 'Наименование подтверждающего документа',
                                            'Дата подтверждающего документа', 'Дата подведения итогов госзакупок',
                                            'ИД заказчика ТРУ', 'БИН заказчика ТРУ', 'Номер договора в системе',
                                            'Финансовый год', 'Форма заключения договора', 'Тип закупки',
                                            'Код валюты договора', 'Сумма заключенного договора без НДС',
                                            'Сумма заключенного договора с НДС', 'Дата заключения договора',
                                            'Общая фактическая сумма договора', 'Тип договора',
                                            'Описание на казахском языке',
                                            'Описание на русском языке', 'Юридический адрес заказчика',
                                            'ИД лота',
                                            'ИД пункта плана', 'Номер пункта плана в договоре', 'Статус плана',
                                            'Способа закупки(плановый)', 'Единица измерения', 'Количество / объем',
                                            'Цена за единицу', 'Общая сумма, утвержденная для закупки',
                                            'Финансовый год в пункте плана',
                                            'Краткая характеристика на русском языке',
                                            'Краткая характеристика на казахском языке',
                                            'Дополнительное описание на русском языке',
                                            'Дополнительное описание на казахском языке',
                                            'ID КАТО', 'Полный адрес поставки на русском языке',
                                            'Полный адрес поставки на казахском языке',
                                            ])

                for contract in data.get('data').get('Contract'):
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

                    if contract.get(
                            'RefContractYearType'):
                        contract_type = contract.get(
                            'RefContractYearType').get(
                            'nameRu')
                    else:
                        contract_type = contract.get(
                            'RefContractYearType')

                    for contractUnit in contract.get('ContractUnits'):
                        if contractUnit.get('Plans') and contractUnit.get('Plans').get('PlansKato'):
                            if contractUnit.get('Plans').get('descRu'):
                                desc_ru2 = contractUnit.get('Plans').get('descRu').strip()
                            else:
                                desc_ru2 = contractUnit.get('Plans').get('descRu')

                            if contractUnit.get('Plans').get('descKz'):
                                desc_kz2 = contractUnit.get('Plans').get('descKz').strip()
                            else:
                                desc_kz2 = contractUnit.get('Plans').get('descKz')

                            if contractUnit.get('Plans').get('extraDescRu'):
                                extra_desc_ru2 = contractUnit.get('Plans').get('extraDescRu').strip()
                            else:
                                extra_desc_ru2 = contractUnit.get('Plans').get('extraDescRu')

                            if contractUnit.get('Plans').get('extraDescKz'):
                                extra_desc_kz2 = contractUnit.get('Plans').get('extraDescKz').strip()
                            else:
                                extra_desc_kz2 = contractUnit.get('Plans').get('extraDescKz')

                            for kato in contractUnit.get('Plans').get('PlansKato'):
                                if kato.get('fullDeliveryPlaceNameRu'):
                                    kato_ru = kato.get('fullDeliveryPlaceNameRu').strip()
                                else:
                                    kato_ru = kato.get('fullDeliveryPlaceNameRu')

                                if kato.get('fullDeliveryPlaceNameKz'):
                                    kato_kz = kato.get('fullDeliveryPlaceNameKz').strip()
                                else:
                                    kato_kz = kato.get('fullDeliveryPlaceNameKz')

                                await file_writer.writerow(
                                    [contract.get('id'),
                                     contract.get(
                                         'trdBuyId'),
                                     contract.get(
                                         'trdBuyNumberAnno'),
                                     contract.get(
                                         'FaktTradeMethods').get('nameRu'),
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
                                     contractUnit.get('lotId'),
                                     contractUnit.get('Plans').get('id'),
                                     contractUnit.get('Plans').get('contractPrevPointId'),
                                     PLAN_STATUS.get(contractUnit.get('Plans').get('refPlnPointStatusId')),
                                     TRADE_METHODS_CODES.get(contractUnit.get('Plans').get('refTradeMethodsId')),
                                     UNITS_CODES.get(contractUnit.get('Plans').get('refUnitsCode')),
                                     contractUnit.get('Plans').get('count'),
                                     contractUnit.get('Plans').get('price'),
                                     contractUnit.get('Plans').get('amount'),
                                     contractUnit.get('Plans').get('plnPointYear'),
                                     desc_ru2,
                                     desc_kz2,
                                     extra_desc_ru2,
                                     extra_desc_kz2,
                                     kato.get('refKatoCode'),
                                     kato_ru,
                                     kato_kz,

                                 ])

                last_id = data.get('extensions').get('pageInfo').get('lastId')

                for x in range(2, contract_page_cnt+1):
                    while True:
                        try:
                            r = await session.post(
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
                                                ContractUnits {
                                                    lotId
                                                    Plans {
                                                        id
                                                        contractPrevPointId
                                                        refPlnPointStatusId
                                                        refTradeMethodsId
                                                        refUnitsCode
                                                        count
                                                        price
                                                        amount
                                                        plnPointYear
                                                        descRu
                                                        descKz
                                                        extraDescKz
                                                        extraDescRu
                                                        PlansKato {
                                                            refKatoCode
                                                            fullDeliveryPlaceNameRu
                                                            fullDeliveryPlaceNameKz
                                                        }
                                                    }
                                                }

                                            }
                                        }
                                    ''',
                                    "variables": {
                                        "limit": 200,
                                        "after": last_id,
                                        "filter": {
                                            "finYear": 2022,
                                        }
                                    },
                                },
                                headers=headers,
                            )

                            data = await r.json()
                            last_id = data.get('extensions').get('pageInfo').get('lastId')
                            print('Page: ', x)

                            for contract in data.get('data').get('Contract'):
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

                                if contract.get(
                                        'RefContractYearType'):
                                    contract_type = contract.get(
                                        'RefContractYearType').get(
                                        'nameRu')
                                else:
                                    contract_type = contract.get(
                                        'RefContractYearType')

                                for contractUnit in contract.get('ContractUnits'):
                                    if contractUnit.get('Plans') and contractUnit.get('Plans').get('PlansKato'):
                                        if contractUnit.get('Plans').get('descRu'):
                                            desc_ru2 = contractUnit.get('Plans').get('descRu').strip()
                                        else:
                                            desc_ru2 = contractUnit.get('Plans').get('descRu')

                                        if contractUnit.get('Plans').get('descKz'):
                                            desc_kz2 = contractUnit.get('Plans').get('descKz').strip()
                                        else:
                                            desc_kz2 = contractUnit.get('Plans').get('descKz')

                                        if contractUnit.get('Plans').get('extraDescRu'):
                                            extra_desc_ru2 = contractUnit.get('Plans').get('extraDescRu').strip()
                                        else:
                                            extra_desc_ru2 = contractUnit.get('Plans').get('extraDescRu')

                                        if contractUnit.get('Plans').get('extraDescKz'):
                                            extra_desc_kz2 = contractUnit.get('Plans').get('extraDescKz').strip()
                                        else:
                                            extra_desc_kz2 = contractUnit.get('Plans').get('extraDescKz')

                                        for kato in contractUnit.get('Plans').get('PlansKato'):
                                            if kato.get('fullDeliveryPlaceNameRu'):
                                                kato_ru = kato.get('fullDeliveryPlaceNameRu').strip()
                                            else:
                                                kato_ru = kato.get('fullDeliveryPlaceNameRu')

                                            if kato.get('fullDeliveryPlaceNameKz'):
                                                kato_kz = kato.get('fullDeliveryPlaceNameKz').strip()
                                            else:
                                                kato_kz = kato.get('fullDeliveryPlaceNameKz')

                                            await file_writer.writerow(
                                                [contract.get('id'),
                                                 contract.get(
                                                     'trdBuyId'),
                                                 contract.get(
                                                     'trdBuyNumberAnno'),
                                                 contract.get(
                                                     'FaktTradeMethods').get('nameRu'),
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
                                                 contractUnit.get('lotId'),
                                                 contractUnit.get('Plans').get('id'),
                                                 contractUnit.get('Plans').get('contractPrevPointId'),
                                                 PLAN_STATUS.get(contractUnit.get('Plans').get('refPlnPointStatusId')),
                                                 TRADE_METHODS_CODES.get(
                                                     contractUnit.get('Plans').get('refTradeMethodsId')),
                                                 UNITS_CODES.get(contractUnit.get('Plans').get('refUnitsCode')),
                                                 contractUnit.get('Plans').get('count'),
                                                 contractUnit.get('Plans').get('price'),
                                                 contractUnit.get('Plans').get('amount'),
                                                 contractUnit.get('Plans').get('plnPointYear'),
                                                 desc_ru2,
                                                 desc_kz2,
                                                 extra_desc_ru2,
                                                 extra_desc_kz2,
                                                 kato.get('refKatoCode'),
                                                 kato_ru,
                                                 kato_kz,

                                             ])
                            break
                        except Exception as err:
                            time.sleep(5)
                            print('contracts_response: error')
                            print('page: ', x)
                            print(err)
    except Exception as err:
        print(err)


async def main():
    await parser()


if __name__ == '__main__':
    asyncio.run(main())
