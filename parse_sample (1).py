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
                                trdBuyNameRu
                                trdBuyNameKz
                                Supplier{
                                	bin
                                	name
                                }
                                signReasonDocName
                                signReasonDocDate
                                trdBuyItogiDatePublic
                                Customer{
                                	bin
                                	name
                                }
                                customerLegalAddress
                                contractNumberSys
                                RefSubjectType{
                                	nameRu
                                }
                                isGu
                                finYear
                                RefCurrency{
                                	name
                                }
                                exchangeRate
                                contractSum
                                contractSumWnds
                                ecEndDate
                                planExecDate
                                faktExecDate
                                faktSum
                                faktSumWnds
                                contractEndDate
                                descriptionKz
                                descriptionRu
                                FaktTradeMethods{
                                	nameRu
                                } 
                                reportStatus
                                reportCreatedAt
                                reportSignAt
                                ContractUnits {
                                    lotId
                                    Plans {
                                        id
                                        subjectBiin
                                        subjectNameRu
                                        nameRu
                                        nameKz
                                        RefTradeMethods{
                                                nameRu
                                        } 
                                        RefUnits{
                                                nameRu
                                        } 
                                        count
                                        price
                                        amount
                                        RefMonths{
                                                nameRu
                                        } 
                                        RefPlnPointStatus{
                                                nameRu
                                        } 
                                        plnPointYear
                                        refEnstruCode
                                        dateCreate
                                        timestamp
                                        descRu
                                        descKz
                                        extraDescRu
                                        extraDescKz
                                        sum1
                                        sum2
                                        sum3
                                        supplyDateRu
                                        prepayment
                                        RefJustification {
                                            nameRu
                                        }
                                        contractPrevPointId
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

            async with aiofiles.open("contracts12.csv", mode="w", encoding='utf-8') as w_file:
                file_writer = aiocsv.AsyncWriter(w_file, delimiter=";",
                                                 lineterminator="\r")
                await file_writer.writerow(['ID договора', 'ID объявления', 'Номер объявления',
                                            'Наименование объявления на русском языке',
                                            'Наименование объявления на казахском языке', 'БИН/ИИН поставщика',
                                            'Наименование поставщика',
                                            'Наименование документа, подтверждающего освнование на заключение',
                                            'Дата подтверждающего документа',
                                            'Дата подведения итогов госзакупок', 'БИН заказчика',
                                            'Наименование заказчика',
                                            'Юридический адрес заказчика', 'Номер договора', 'Вид предмета закупок',
                                            'Признак ГУ', 'Финансовый год', 'Код валюты договора',
                                            'Курс валюты', 'Сумма заключенного договора без НДС',
                                            'Сумма заключенного договора с НДС',
                                            'Срок действия', 'Планируемая дата исполнения',
                                            'Фактическая дата исполнения',
                                            'Сумма фактических выплат без ндс', 'Сумма фактических выплат с ндс',
                                            'Дата окончания договора',
                                            'Описание на казахском языке', 'Описание на русском языке',
                                            'Фактический способ закупки',
                                            'Статус отчета о ГЗ из одного источника',
                                            'Дата создания отчета о ГЗ из одного источника',
                                            'Дата подписания отчета о ГЗ из одного источника'
                                            'ID лота', 'ID пункта плана', 'БИН заказчика',
                                            'Наименование заказчика', 'Наименование на русском',
                                            'Наименование на казахском',
                                            'Способа закупки плана', 'Единица измерения', 'Количество / объем',
                                            'Цена за единицу', 'Общая сумма, утвержденная для закупки',
                                            'Планируемый срок закупки',
                                            'Статус пункта плана', 'Финансовый год в пункте плана', 'Код КТРУ',
                                            'Дата создания записи', 'Дата изменения записи',
                                            'Краткая характеристика на русском языке',
                                            'Краткая характеристика на казахском языке',
                                            'Дополнительное описание на русском языке',
                                            'Дополнительное описание на казахском языке',
                                            'Планируемая сумма на 1 год', 'Планируемая сумма на 2 год',
                                            'Планируемая сумма на 3 год',
                                            'Срок поставки', 'Размер авансного платежа',
                                            'Обоснование применения способа закупки',
                                            'Номер пункта плана в договоре', 'ID КАТО',
                                            'Полный адрес поставки на русском языке',
                                            'Полный адрес поставки на казахском языке',
                                            ])

                for contract in data.get('data').get('Contract'):
                    if contract.get('signReasonDocName'):
                        signReasonName = contract.get('signReasonDocName').strip()
                    else:
                        signReasonName = contract.get('signReasonDocName')

                    if contract.get('descriptionKz'):
                        desc_kz1 = contract.get('descriptionKz').strip()
                    else:
                        desc_kz1 = contract.get('descriptionKz')

                    if contract.get('descriptionRu'):
                        desc_ru1 = contract.get('descriptionRu').strip()
                    else:
                        desc_ru1 = contract.get('descriptionRu')

                    if contract.get('customerLegalAddress'):
                        customer_addr = contract.get('customerLegalAddress').strip()
                    else:
                        customer_addr = contract.get('customerLegalAddress')

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
                                extra_desc_ru2 = extra_desc_ru2.replace("\n", "")
                                extra_desc_ru2 = extra_desc_ru2.replace("\r", "")
                            else:
                                extra_desc_ru2 = contractUnit.get('Plans').get('extraDescRu')

                            if contractUnit.get('Plans').get('extraDescKz'):
                                extra_desc_kz2 = contractUnit.get('Plans').get('extraDescKz').strip()
                                extra_desc_kz2 = extra_desc_kz2.replace("\n", "")
                                extra_desc_kz2 = extra_desc_kz2.replace("\r", "")
                            else:
                                extra_desc_kz2 = contractUnit.get('Plans').get('extraDescKz')

                            for kato in contractUnit.get('Plans').get('PlansKato'):
                                if kato.get('fullDeliveryPlaceNameRu'):
                                    kato_ru = kato.get('fullDeliveryPlaceNameRu').strip()
                                    kato_ru = kato_ru.replace("\n", "")
                                    kato_ru = kato_ru.replace("\r", "")
                                else:
                                    kato_ru = kato.get('fullDeliveryPlaceNameRu')

                                if kato.get('fullDeliveryPlaceNameKz'):
                                    kato_kz = kato.get('fullDeliveryPlaceNameKz').strip()
                                    kato_kz = kato_kz.replace("\n", "")
                                    kato_kz = kato_kz.replace("\r", "")
                                else:
                                    kato_kz = kato.get('fullDeliveryPlaceNameKz')

                                await file_writer.writerow(
                                    [contract.get('id'),
                                     contract.get('trdBuyId'),
                                     contract.get('trdBuyNumberAnno'),
                                     contract.get('trdBuyNameRu'),
                                     contract.get('trdBuyNameKz'),
                                     contract.get('Supplier').get('bin'),
                                     contract.get('Supplier').get('name'),
                                     signReasonName,
                                     contract.get('signReasonDocDate'),
                                     contract.get('trdBuyItogiDatePublic'),
                                     contract.get('Customer').get('bin'),
                                     contract.get('Customer').get('name'),
                                     customer_addr,
                                     contract.get('contractNumberSys'),
                                     contract.get('RefSubjectType').get('nameRu'),
                                     contract.get('isGu'),
                                     contract.get('finYear'),
                                     contract.get('RefCurrency').get('name'),
                                     contract.get('exchangeRate'),
                                     contract.get('contractSum'),
                                     contract.get('contractSumWnds'),
                                     contract.get('ecEndDate'),
                                     contract.get('planExecDate'),
                                     contract.get('faktExecDate'),
                                     contract.get('faktSum'),
                                     contract.get('faktSumWnds'),
                                     contract.get('contractEndDate'),
                                     desc_kz1,
                                     desc_ru1,
                                     contract.get('FaktTradeMethods').get('nameRu'),
                                     contract.get('reportStatus'),
                                     contract.get('reportCreatedAt'),
                                     contract.get('reportSignAt'),
                                     contractUnit.get('lotId'),
                                     contractUnit.get('Plans').get('id'),
                                     contractUnit.get('Plans').get('subjectBiin'),
                                     contractUnit.get('Plans').get('subjectNameRu'),
                                     contractUnit.get('Plans').get('nameRu'),
                                     contractUnit.get('Plans').get('nameKz'),
                                     contractUnit.get('Plans').get('RefTradeMethods').get('nameRu'),
                                     contractUnit.get('Plans').get('RefUnits').get('nameRu'),
                                     contractUnit.get('Plans').get('count'),
                                     contractUnit.get('Plans').get('price'),
                                     contractUnit.get('Plans').get('amount'),
                                     contractUnit.get('Plans').get('RefMonths').get('nameRu'),
                                     contractUnit.get('Plans').get('RefPlnPointStatus').get('nameRu'),
                                     contractUnit.get('Plans').get('plnPointYear'),
                                     contractUnit.get('Plans').get('refEnstruCode'),
                                     contractUnit.get('Plans').get('dateCreate'),
                                     contractUnit.get('Plans').get('timestamp'),
                                     desc_ru2,
                                     desc_kz2,
                                     extra_desc_ru2,
                                     extra_desc_kz2,
                                     contractUnit.get('Plans').get('sum1'),
                                     contractUnit.get('Plans').get('sum2'),
                                     contractUnit.get('Plans').get('sum3'),
                                     contractUnit.get('Plans').get('supplyDateRu'),
                                     contractUnit.get('Plans').get('prepayment'),
                                     contractUnit.get('Plans').get('refJustification').get('nameRu'),
                                     contractUnit.get('Plans').get('contractPrevPointId'),
                                     kato.get('refKatoCode'),
                                     kato_ru,
                                     kato_kz,
                                     ])

                last_id = data.get('extensions').get('pageInfo').get('lastId')

                for x in range(2, 20):
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
                                                trdBuyNameRu
                                                trdBuyNameKz
                                                Supplier{
                                                    bin
                                                    name
                                                }
                                                signReasonDocName
                                                signReasonDocDate
                                                trdBuyItogiDatePublic
                                                Customer{
                                                    bin
                                                    name
                                                }
                                                customerLegalAddress
                                                contractNumberSys
                                                RefSubjectType{
                                                    nameRu
                                                }
                                                isGu
                                                finYear
                                                RefCurrency{
                                                    name
                                                }
                                                exchangeRate
                                                contractSum
                                                contractSumWnds
                                                ecEndDate
                                                planExecDate
                                                faktExecDate
                                                faktSum
                                                faktSumWnds
                                                contractEndDate
                                                descriptionKz
                                                descriptionRu
                                                FaktTradeMethods{
                                                    nameRu
                                                } 
                                                reportStatus
                                                reportCreatedAt
                                                reportSignAt
                                                ContractUnits {
                                                    lotId
                                                    Plans {
                                                        id
                                                        subjectBiin
                                                        subjectNameRu
                                                        nameRu
                                                        nameKz
                                                        RefTradeMethods{
                                                                nameRu
                                                        } 
                                                        RefUnits{
                                                                nameRu
                                                        } 
                                                        count
                                                        price
                                                        amount
                                                        RefMonths{
                                                                nameRu
                                                        } 
                                                        RefPlnPointStatus{
                                                                nameRu
                                                        } 
                                                        plnPointYear
                                                        refEnstruCode
                                                        dateCreate
                                                        timestamp
                                                        descRu
                                                        descKz
                                                        extraDescRu
                                                        extraDescKz
                                                        sum1
                                                        sum2
                                                        sum3
                                                        supplyDateRu
                                                        prepayment
                                                        RefJustification {
                                                            nameRu
                                                        }
                                                        contractPrevPointId
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
                                if contract.get('signReasonDocName'):
                                    signReasonName = contract.get('signReasonDocName').strip()
                                else:
                                    signReasonName = contract.get('signReasonDocName')

                                if contract.get('descriptionKz'):
                                    desc_kz1 = contract.get('descriptionKz').strip()
                                else:
                                    desc_kz1 = contract.get('descriptionKz')

                                if contract.get('descriptionRu'):
                                    desc_ru1 = contract.get('descriptionRu').strip()
                                else:
                                    desc_ru1 = contract.get('descriptionRu')

                                if contract.get('customerLegalAddress'):
                                    customer_addr = contract.get('customerLegalAddress').strip()
                                else:
                                    customer_addr = contract.get('customerLegalAddress')

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
                                            extra_desc_ru2 = extra_desc_ru2.replace("\n", "")
                                            extra_desc_ru2 = extra_desc_ru2.replace("\r", "")
                                        else:
                                            extra_desc_ru2 = contractUnit.get('Plans').get('extraDescRu')

                                        if contractUnit.get('Plans').get('extraDescKz'):
                                            extra_desc_kz2 = contractUnit.get('Plans').get('extraDescKz').strip()
                                            extra_desc_kz2 = extra_desc_kz2.replace("\n", "")
                                            extra_desc_kz2 = extra_desc_kz2.replace("\r", "")
                                        else:
                                            extra_desc_kz2 = contractUnit.get('Plans').get('extraDescKz')

                                        for kato in contractUnit.get('Plans').get('PlansKato'):
                                            if kato.get('fullDeliveryPlaceNameRu'):
                                                kato_ru = kato.get('fullDeliveryPlaceNameRu').strip()
                                                kato_ru = kato_ru.replace("\n", "")
                                                kato_ru = kato_ru.replace("\r", "")
                                            else:
                                                kato_ru = kato.get('fullDeliveryPlaceNameRu')

                                            if kato.get('fullDeliveryPlaceNameKz'):
                                                kato_kz = kato.get('fullDeliveryPlaceNameKz').strip()
                                                kato_kz = kato_kz.replace("\n", "")
                                                kato_kz = kato_kz.replace("\r", "")
                                            else:
                                                kato_kz = kato.get('fullDeliveryPlaceNameKz')

                                            await file_writer.writerow(
                                                [contract.get('id'),
                                                 contract.get('trdBuyId'),
                                                 contract.get('trdBuyNumberAnno'),
                                                 contract.get('trdBuyNameRu'),
                                                 contract.get('trdBuyNameKz'),
                                                 contract.get('Supplier').get('bin'),
                                                 contract.get('Supplier').get('name'),
                                                 signReasonName,
                                                 contract.get('signReasonDocDate'),
                                                 contract.get('trdBuyItogiDatePublic'),
                                                 contract.get('Customer').get('bin'),
                                                 contract.get('Customer').get('name'),
                                                 customer_addr,
                                                 contract.get('contractNumberSys'),
                                                 contract.get('RefSubjectType').get('nameRu'),
                                                 contract.get('isGu'),
                                                 contract.get('finYear'),
                                                 contract.get('RefCurrency').get('name'),
                                                 contract.get('exchangeRate'),
                                                 contract.get('contractSum'),
                                                 contract.get('contractSumWnds'),
                                                 contract.get('ecEndDate'),
                                                 contract.get('planExecDate'),
                                                 contract.get('faktExecDate'),
                                                 contract.get('faktSum'),
                                                 contract.get('faktSumWnds'),
                                                 contract.get('contractEndDate'),
                                                 desc_kz1,
                                                 desc_ru1,
                                                 contract.get('FaktTradeMethods').get('nameRu'),
                                                 contract.get('reportStatus'),
                                                 contract.get('reportCreatedAt'),
                                                 contract.get('reportSignAt'),
                                                 contractUnit.get('lotId'),
                                                 contractUnit.get('Plans').get('id'),
                                                 contractUnit.get('Plans').get('subjectBiin'),
                                                 contractUnit.get('Plans').get('subjectNameRu'),
                                                 contractUnit.get('Plans').get('nameRu'),
                                                 contractUnit.get('Plans').get('nameKz'),
                                                 contractUnit.get('Plans').get('RefTradeMethods').get('nameRu'),
                                                 contractUnit.get('Plans').get('RefUnits').get('nameRu'),
                                                 contractUnit.get('Plans').get('count'),
                                                 contractUnit.get('Plans').get('price'),
                                                 contractUnit.get('Plans').get('amount'),
                                                 contractUnit.get('Plans').get('RefMonths').get('nameRu'),
                                                 contractUnit.get('Plans').get('RefPlnPointStatus').get('nameRu'),
                                                 contractUnit.get('Plans').get('plnPointYear'),
                                                 contractUnit.get('Plans').get('refEnstruCode'),
                                                 contractUnit.get('Plans').get('dateCreate'),
                                                 contractUnit.get('Plans').get('timestamp'),
                                                 desc_ru2,
                                                 desc_kz2,
                                                 extra_desc_ru2,
                                                 extra_desc_kz2,
                                                 contractUnit.get('Plans').get('sum1'),
                                                 contractUnit.get('Plans').get('sum2'),
                                                 contractUnit.get('Plans').get('sum3'),
                                                 contractUnit.get('Plans').get('supplyDateRu'),
                                                 contractUnit.get('Plans').get('prepayment'),
                                                 contractUnit.get('Plans').get('refJustification').get('nameRu'),
                                                 contractUnit.get('Plans').get('contractPrevPointId'),
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
