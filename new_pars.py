import requests


import csv


URL = "https://ows.goszakup.gov.kz/v3/lots"
announce_URL = "https://ows.goszakup.gov.kz/v3/trd-buy/"
contract_URL = "https://ows.goszakup.gov.kz/v3/contract/"
subject_type = "https://ows.goszakup.gov.kz/v3/refs/ref_subject_type"
plans_URL = "https://ows.goszakup.gov.kz/v3/plans/all"
plan_URL = "https://ows.goszakup.gov.kz/v3/plans/view/"
bin_URL = "https://ows.goszakup.gov.kz/v3/subject/biin/"

headers = dict()
headers["Authorization"] = "Bearer 3eaae6dd49f1ab32c1421c9db58a3a59"
headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Safari/605.1.15"
headers["Content-Type"] = "application/json"

# try:
#     r = requests.get("https://ows.goszakup.gov.kz/v3/refs/ref_trade_methods",
#     headers=headers,
#     verify=False)
#     print(r)
#     data = r.json()
#     print(data)
# except Exception as err:
#     print(err)
year = True

for dd in range(1, 2):
    with open(f"{dd}.csv", mode="w", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=";",
                                 lineterminator="\r")
        file_writer.writerow(['БИН организации', 'Название органзиции', 'КАТО', 'Полный адрес поставки',
                              'Дата начала', 'Дата изменения',
                              ])

        try:
            # for x in range((dd-1)*3000 +1, dd*3000): #55509
            for x in range(1, 100): #55509
                try:
                    PARAMS = {'limit': 500, 'page' : x}

                    try:
                        r = requests.get(url = plans_URL, params = PARAMS, headers = headers, verify = False)
                    except Exception as err:
                        print(x, err)

                    data = r.json()
                    data = data['items']
                    for y in data:
                        pp = requests.get(plan_URL+str(y.get('id')), headers = headers, verify = False,)
                        p = pp.json()
                        if p.get('pln_point_year') == 2022:
                            if p.get('ref_pln_point_status_id') == 9 and p.get('ref_trade_methods_id') in (22,
                                                                                                          32,
                                                                                                          120,
                                                                                                          121,
                                                                                                          2,
                                                                                                          126):
                                for j in p.get('kato'):
                                    if j.get('ref_kato_code')[:2] in ("71", "75") or j.get('ref_kato_code')[:4] == "1170":
                                        cc = requests.get(bin_URL+p.get('subject_biin'), headers = headers, verify = False,)
                                        c = cc.json()
                                        file_writer.writerow([p.get('subject_biin'), c.get('name_ru'), j.get('ref_kato_code'),
                                                              j.get('full_delivery_place_name_ru'),
                                                              p.get('date_create'), p.get('timestamp'),
                                                             ])
                        else:
                            print('Год 2022 закончился')
                except:
                    print('error page number: ', x)
        except:
            pass