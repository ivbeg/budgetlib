# -*- coding: utf-8 -*-
import os
import requests
import json
import csv
import datetime

FULLURLPAT = 'http://budget.gov.ru/epbs/reporting/Data?uuid=309a092f-777d-43ea-9f83-4b0370c7dcc2&dataVersion=15.03.2019%2006.58.00.271&dsCode=EBPS_177_001_BA_GridData&EBPS_177_001_BA_SearchIndFilter=kvsrName&EPBS_177_TreeFilter=1&EPBS_177_periodFilter=2019&EPBS_177_budgetFilter=00000001&EBPS_177_001_BA_SearchFilter=&SBR_paramPeriod=2019-06-05T00:00:00.000Z&_dc=1560852158712&limit=500'
BASELIMIT = 500
keys = ['name', 'grbs', 'topic', 'subtopic', 'csr_program', 'csr_article', 'vr', 'budget2019', 'budget2020', 'budget2021']

def extract_full_budget_data(adate):
    """Exctract budget data from budget.gov.ru API"""
    start = 0
    page = 1
    out = []
    while True:
        print('Downloading data for %s page %d' % (str(adate), page))
        url = FULLURLPAT + '&rangeDatePickerFilter=%s' % (adate.strftime('%d.%m.%Y')) + '&page=%d' % (page) + '&start=%d' % start
        r = requests.get(url)
        result = r.json()
        if 'data' not in result:
            break
        for res in result['data']:
            out.append(dict(zip(keys, res)))
        if len(result['data']) != BASELIMIT:
            break
        page += 1
        start += BASELIMIT
    return out

def save(filename, data):
    wr = csv.DictWriter(open(filename, 'w', encoding='utf8'), fieldnames=keys) 
    wr.writeheader()
    for r in data:
        wr.writerow(r)

def save_all(filepath='data/raw/'):
    start_date = datetime.date(2019, 1, 1)
    end_date = datetime.datetime.now().date()
    delta = end_date - start_date
    daterange = []
    for i in range(delta.days + 1):
        ad = start_date + datetime.timedelta(days=i)
        daterange.append(ad)
    for ad in daterange:
        filename = str(ad) + '.csv'
        fullname = filepath + filename   
        if os.path.exists(fullname): continue
#        print('Saving %s' % (filename))
        data = extract_full_budget_data(ad)
        save(fullname, data)


if __name__ == "__main__":
    save_all()