# -*- coding: utf-8 -*-
import pandas as pd

from .extract import get_full_budget_data

def programs_date_diff(dates, frames=None):
    """Возвращает таблицу сравнения по расходам на программы между датами"""
    dfs = []
    unique_p = set()
    if frames:
        dframe = zip(dates, frames)
    else:
        frames = []
        for d in dates:
            frames.append(get_full_budget_data(d))
        dframe = zip(dates, frames)
    for d, df_f in dframe:
        df_s = \
        df_f.loc[df_f['vr'].isnull()].loc[df_f['csr_program'].isnull() == False][df_f['csr_program'].str[-3:] == '000'][
            df_f['name'].str.contains('программа') == True]
        unique_p = unique_p.union(df_s['csr_program'].unique())
        dfs.append(df_s)

    difftable = []
    for ug in unique_p:
        record = {'program': ug}
        for i in range(0, len(dates), 1):
            o = dfs[i].loc[dfs[i]['csr_program'] == ug]
            if i == 0:
                record['name'] = o['name'].values[0]
            dname = str(dates[i]).replace('.', '_')
            record[dname] = sum(o['budget2019'].values)
            record[dname + '_d'] = (record[dname] - record[str(dates[i - 1]).replace('.', '_')]) if i > 0 else 0
            record[dname + '_ds'] = (record[dname] - record[str(dates[i - 1]).replace('.', '_')]) * 100.0 / record[
                str(dates[i - 1]).replace('.', '_')] if i > 0 else 0
        #        record['diff'] = record['right'] - record['left']
        #        record['diff_share'] = (record['right'] - record['left']) * 100.0 / record['left'] if record['left'] > 0 else 0
        difftable.append(record)
    fields = ['program', 'name', ]
    for i in range(0, len(dates), 1):
        d = dates[i]
        if i > 0:
            fields.append(str(d).replace('.', '_') + '_d')
            fields.append(str(d).replace('.', '_') + '_ds')
        fields.append(str(d).replace('.', '_'))
    dfdiff = pd.DataFrame(difftable, columns=fields)
    return dfdiff

def projects_date_diff(dates, frames=None):
    """Возвращает таблицу сравнения по расходам на национальные проекты между датами"""
    dfs = []
    unique_p = set()
    if frames:
        dframe = zip(dates, frames)
    else:
        frames = []
        for d in dates:
            frames.append(get_full_budget_data(d))
        dframe = zip(dates, frames)
    for d, df_f in dframe:
        df_s = df_f.loc[df_f['vr'].isnull()].loc[df_f['csr_article'].isnull() == False][df_f['csr_article'].str[1:] == '0000'][
    df_f['csr_article'].str[0] != '0'][df_f['csr_article'].str[0] != '9']

        unique_p = unique_p.union(df_s['csr_article'].unique())
        dfs.append(df_s)
    difftable = []
    for ug in unique_p:
        record = {'project': ug}
        for i in range(0, len(dates), 1):
            o = dfs[i].loc[dfs[i]['csr_article'] == ug]
            if i == 0:
                record['name'] = o['name'].values[0]
            dname = str(dates[i]).replace('.', '_')
            record[dname] = sum(o['budget2019'].values)
            record[dname + '_d'] = (record[dname] - record[str(dates[i - 1]).replace('.', '_')]) if i > 0 else 0
            record[dname + '_ds'] = (record[dname] - record[str(dates[i - 1]).replace('.', '_')]) * 100.0 / record[
                str(dates[i - 1]).replace('.', '_')] if i > 0 else 0
        #        record['diff'] = record['right'] - record['left']
        #        record['diff_share'] = (record['right'] - record['left']) * 100.0 / record['left'] if record['left'] > 0 else 0
        difftable.append(record)
    fields = ['project', 'name', ]
    for i in range(0, len(dates), 1):
        d = dates[i]
        if i > 0:
            fields.append(str(d).replace('.', '_') + '_d')
            fields.append(str(d).replace('.', '_') + '_ds')
        fields.append(str(d).replace('.', '_'))
    dfdiff = pd.DataFrame(difftable, columns=fields)
    return dfdiff


def grbs_date_diff(dates, frames=None):
    """Возвращает таблицу сравнения расходов по ГРБС между датами"""
    dfs = []
    unique_grbs = set()
    if frames:
        dframe = zip(dates, frames)
    else:
        frames = []
        for d in dates:
            frames.append(get_full_budget_data(d))
        dframe = zip(dates, frames)
    for d, df_f in dframe:
        df_s = df_f.loc[df_f['topic'].isnull()].loc[df_f['grbs'].isnull() == False][['name', 'grbs', 'budget2019']]
        unique_grbs = unique_grbs.union(df_s['grbs'].unique())
        dfs.append(df_s)

    difftable = []
    for ug in unique_grbs:
        record = {'grbs': ug}
        for i in range(0, len(dates), 1):
            o = dfs[i].loc[dfs[i]['grbs'] == ug]
            if i == 0:
                record['name'] = o['name'].values[0]
            dname = str(dates[i]).replace('.', '_')
            record[dname] = o['budget2019'].values[0]
            record[dname + '_d'] = (record[dname] - record[str(dates[i - 1]).replace('.', '_')]) if i > 0 else 0
            record[dname + '_ds'] = (record[dname] - record[str(dates[i - 1]).replace('.', '_')]) * 100.0 / record[
                str(dates[i - 1]).replace('.', '_')] if i > 0 else 0
        #        record['diff'] = record['right'] - record['left']
        #        record['diff_share'] = (record['right'] - record['left']) * 100.0 / record['left'] if record['left'] > 0 else 0
        difftable.append(record)
    fields = ['grbs', 'name', ]
    for i in range(0, len(dates), 1):
        d = dates[i]
        if i > 0:
            fields.append(str(d).replace('.', '_') + '_d')
            fields.append(str(d).replace('.', '_') + '_ds')
        fields.append(str(d).replace('.', '_'))
    dfdiff = pd.DataFrame(difftable, columns=fields)
    return dfdiff

def full_date_diff(date1, date2, frames=None):
    """Формируем таблицу разницы в сводных росписях бюджета в строках"""
    dfs = []
    dates = [date1, date2]
    if frames:
        dframe = zip(dates, frames)
    else:
        frames = []
        for d in dates:
            frames.append(get_full_budget_data(d))
        dframe = zip(dates, frames)
    for d, df_f in dframe:
        df_f = get_full_budget_data(d)
        row_ids = []
        for index, row in df_f.iterrows():
            id = []
            for k in ['grbs', 'topic', 'subtopic', 'csr_program', 'csr_article', 'vr']:
                id.append(row[k] if row[k] is not None else "")
            id = '_'.join(id)
            row_ids.append(id)
        df_f['id'] = row_ids
        df_f.set_index('id')
        dfs.append(df_f)

    df_left = dfs[0]
    df_right = dfs[1]
    difftable = []
    for index, rec_left in df_left.iterrows():
        query = df_right.loc[df_right['id'] == rec_left['id']]
#        query = df_right.query('id == "%s"' % rec_left['id'])
        if len(query['budget2019'].values) == 0:
            print("Removed %s" % rec_left['id'])
            rec_left['status'] = 'removed'
            rec_left['change'] = -rec_left['budget2019']
            rec_left['change_share'] = 0
            difftable.append(rec_left)
            df_left.drop([index], inplace=True)
        elif rec_left['budget2019'] != query['budget2019'].values[0]:
            rec_left['status'] = 'changed'
            rec_left['change'] = query['budget2019'].values[0] - rec_left['budget2019']
            rec_left['change_share'] = 100.0* (query['budget2019'].values[0] - rec_left['budget2019']) / rec_left['budget2019']
            rec_left['budget2019'] = query['budget2019'].values[0]
            difftable.append(rec_left)
            df_left.drop([index], inplace=True)
            df_right.drop([query.index.values[0]], inplace=True)
        else:
            df_left.drop([index], inplace=True)
            df_right.drop([query.index.values[0]], inplace=True)
    print(len(df_left), len(df_right))
    for index, rec_right in df_right.iterrows():
        #        print(index)
        rec_right['status'] = 'added'
        rec_right['change'] = rec_right['budget2019']
        rec_right['change_share'] = 0
        difftable.append(rec_right)

    fields = ['status', 'change', 'change_share', 'name', 'grbs', 'topic', 'subtopic', 'csr_program', 'csr_article', 'vr', 'budget2019']
    dfdiff = pd.DataFrame(difftable, columns=fields)
    return dfdiff


def vr_date_diff(dates, frames=None):
    """Формируем таблицу изменений в видах расходах между датами"""
    dfs = []
    unique_p = set()
    if frames:
        dframe = zip(dates, frames)
    else:
        frames = []
        for d in dates:
            frames.append(get_full_budget_data(d))
        dframe = zip(dates, frames)
    for d, df_f in dframe:
        df_s = df_f.loc[df_f['vr'].isnull() == False]
        unique_p = unique_p.union(df_s['vr'].unique())
        dfs.append(df_s)

    difftable = []
    for ug in unique_p:
        record = {'vr': ug}
        for i in range(0, len(dates), 1):
            o = dfs[i].loc[dfs[i]['vr'] == ug]
            if i == 0:
                record['name'] = o['name'].values[0]
            dname = str(dates[i]).replace('.', '_')
            record[dname] = sum(o['budget2019'].values)
            record[dname + '_d'] = (record[dname] - record[str(dates[i - 1]).replace('.', '_')]) if i > 0 else 0
            record[dname + '_ds'] = (record[dname] - record[str(dates[i - 1]).replace('.', '_')]) * 100.0 / record[
                str(dates[i - 1]).replace('.', '_')] if i > 0 else 0
        #        record['diff'] = record['right'] - record['left']
        #        record['diff_share'] = (record['right'] - record['left']) * 100.0 / record['left'] if record['left'] > 0 else 0
        difftable.append(record)
    fields = ['vr', 'name', ]
    for i in range(0, len(dates), 1):
        d = dates[i]
        if i > 0:
            fields.append(str(d).replace('.', '_') + '_d')
            fields.append(str(d).replace('.', '_') + '_ds')
        fields.append(str(d).replace('.', '_'))
    dfdiff = pd.DataFrame(difftable, columns=fields)
    return dfdiff