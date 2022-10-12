# -*- coding: utf-8 -*-
"""Функции по преобразованию срезов сводной бюджетной росписи в по госпрограммам, нац проектам, ГРБС и видам расходов"""
import pandas as pd

from .extract import get_full_budget_data

def programs_view(adate, frame=None, programs_only=False):
    """Возвращает таблицу списка госпрограмм"""
    dfs = None
    unique_p = set()
    if frame is not None:
        frame = get_full_budget_data(adate)
    if programs_only:
        df_s = \
        frame.loc[frame['vr'].isnull()].loc[frame['csr_program'].isnull() == False][frame['csr_program'].str[-3:] == '000'][
            frame['name'].str.contains('программа') == True]
    else:
        df_s = \
            frame.loc[frame['vr'].isnull()].loc[frame['csr_program'].isnull() == False][
                frame['csr_program'].str[-3:] == '000']
    unique_p = df_s['csr_program'].unique()

    atable = []
    for ug in unique_p:
        record = {'program': ug}
        o = df_s.loc[df_s['csr_program'] == ug]
        record['name'] = o['name'].values[0]
        record['summ'] = sum(o['budget2019'].values)

        atable.append(record)
    fields = ['program', 'name', 'summ']
    findf = pd.DataFrame(atable, columns=fields)
    return findf


def projects_view(adate, frame=None):
    """Возвращает таблицу списка национальных проектов"""
    dfs = None
    unique_p = set()
    if frame is not None:
        frame = get_full_budget_data(adate)
    df_s = frame.loc[frame['vr'].isnull()].loc[frame['csr_article'].isnull() == False][frame['csr_article'].str[1:] == '0000'][
    frame['csr_article'].str[0] != '0'][frame['csr_article'].str[0] != '9']
    unique_p = df_s['csr_article'].unique()

    atable = []
    for ug in unique_p:
        record = {'project': ug}
        o = df_s.loc[df_s['csr_article'] == ug]
        record['name'] = o['name'].values[0]
        record['summ'] = sum(o['budget2019'].values)

        atable.append(record)
    fields = ['project', 'name', 'summ']
    findf = pd.DataFrame(atable, columns=fields)
    return findf

def vr_view(adate, frame=None):
    """Возвращает таблицу по видам расходов"""
    dfs = None
    unique_p = set()
    if frame is not None:
        frame = get_full_budget_data(adate)
    df_s = frame.loc[frame['vr'].isnull() == False]

    unique_p = df_s['vr'].unique()

    atable = []
    for ug in unique_p:
        record = {'vr': ug}
        o = df_s.loc[df_s['vr'] == ug]
        record['name'] = o['name'].values[0]
        record['summ'] = sum(o['budget2019'].values)

        atable.append(record)
    fields = ['vr', 'name', 'summ']
    findf = pd.DataFrame(atable, columns=fields)
    return findf


def grbs_view(adate, frame=None):
    """Возвращает таблицу списка ГРБС с суммами"""
    dfs = None
    unique_p = set()
    if frame is not None:
        frame = get_full_budget_data(adate)
    df_s = frame.loc[frame['topic'].isnull()].loc[frame['grbs'].isnull() == False][['name', 'grbs', 'budget2019']]
    unique_p = df_s['grbs'].unique()

    atable = []
    for ug in unique_p:
        record = {'grbs': ug}
        o = df_s.loc[df_s['grbs'] == ug]
        record['name'] = o['name'].values[0]
        record['summ'] = o['budget2019'].values[0]

        atable.append(record)
    fields = ['program', 'name', 'summ']
    findf = pd.DataFrame(atable, columns=fields)
    return findf


def projects_vr_view(adate, frame=None, ):
    """Создаёт таблицу матрицы по каждому нац. проекту и объёмам расходов по каждому виду расходов"""
    if frame is not None:
        frame = get_full_budget_data(adate)

    df_s = frame.loc[frame['vr'].isnull()].loc[frame['csr_article'].isnull() == False][frame['csr_article'].str[1:] == '0000'][
    frame['csr_article'].str[0] != '0'][frame['csr_article'].str[0] != '9']
    unique_r = df_s['csr_article'].unique()
    unique_vr = frame.loc[frame['vr'].isnull() == False]['vr'].unique()
    unique_vr.sort()

    atable = []
    for ug in unique_r:
        record = {'grbs': ug}
        o = df_s.loc[df_s['csr_article'] == ug]
        record['name'] = o['name'].values[0]
        record['total'] = o['budget2019'].values[0]
        for vr in unique_vr:
            vrrec = frame.loc[frame['csr_article'] == ug].loc[frame['vr'] == vr]['budget2019']
            record[vr] = sum(vrrec)
        atable.append(record)
    fields = ['project', 'name', 'total']
    fields.extend(unique_vr)
    findf = pd.DataFrame(atable, columns=fields)
    return findf


def grbs_vr_view(adate, frame=None, ):
    """Создаёт таблицу матрицы по каждому ГРБС и объёмам расходов по каждому виду расходов"""
    if frame is not None:
        frame = get_full_budget_data(adate)
    df_s = frame.loc[frame['topic'].isnull()].loc[frame['grbs'].isnull() == False][['name', 'grbs', 'budget2019']]
    unique_grbs = df_s['grbs'].unique()
    unique_vr = frame.loc[frame['vr'].isnull() == False]['vr'].unique()
    unique_vr.sort()

    atable = []
    for ug in unique_grbs:
        record = {'grbs': ug}
        o = df_s.loc[df_s['grbs'] == ug]
        record['name'] = o['name'].values[0]
        record['total'] = o['budget2019'].values[0]
        for vr in unique_vr:
            vrrec = frame.loc[frame['grbs'] == ug].loc[frame['vr'] == vr]['budget2019']
            record[vr] = sum(vrrec)
        atable.append(record)
    fields = ['grbs', 'name', 'total']
    fields.extend(unique_vr)
    findf = pd.DataFrame(atable, columns=fields)
    return findf

