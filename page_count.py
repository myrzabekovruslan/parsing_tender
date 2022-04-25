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

include_bin = {
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
last_id = data.get('extensions').get('pageInfo').get('lastId')

id_list = []

for i in range(1600):
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
    if i % 265 == 0:
        id_list.append(last_id)
    last_id = data.get('extensions').get('pageInfo').get('lastId')

print(id_list)

# [15080813, 14939314, 14821926, 14696083, 14578730, 14450271, 14229328]