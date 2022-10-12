# -*- coding: utf-8 -*-
import csv
import pandas as pd

def get_full_budget_data(adate, filepath='data/raw'):
    """Returns cached data from data/raw as pd.DataFrame"""
    table = []
    reader = csv.DictReader(open(filepath + '%s.csv' % (str(adate)), 'r', encoding='utf-8'))
    for r in reader:
        for k in reader.fieldnames:
            if len(r[k]) == 0:
                r[k] = None
        for k in ['budget2019', 'budget2020', 'budget2021']:
            r[k] = float(r[k])
        table.append(r)
    df = pd.DataFrame(table, columns=reader.fieldnames)
    return df

