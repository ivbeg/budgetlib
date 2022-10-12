# -*- coding: utf-8 -*-
from .diff import grbs_date_diff

def humanize_diff_grbs(left, right, without_unchanged=False):
    """Сравнивает сводную бюджетную роспись между двумя датами и возвращает человекопонятный текст в формате markdown
    """
    dates = [left, right]
    ad = grbs_date_diff(dates)

    left_f = str(left).replace('.', '_')
    right_f = str(right).replace('.', '_')
    ds_f = str(right).replace('.', '_') + '_ds'
    d_f = str(right).replace('.', '_') + '_d'
    ad = ad.sort_values(by=ds_f, ascending=False)

    groupnames = {}
    groups = {'great': [], 'medium': [], 'little': [], 'nochange': []}
    for index, r in ad.iterrows():
        rec = {'name': r['name'], 'base': r[left_f], 'change': r[d_f], 'share': r[ds_f]}
        r['asc'] = 1 if rec['change'] > 0 else -1
        if r[ds_f] == 0:
            grpname = 'nochange'
            r['asc'] = 0
        elif abs(r[ds_f]) < 10:
            grpname = 'little'
        elif abs(r[ds_f]) >= 10 and abs(r[ds_f]) < 50:
            grpname = 'medium'
        else:
            grpname = 'great'
        groups[grpname].append(rec)

    text = """# Изменения в сводной бюджетной росписи с %s по %s
    """ % (str(left), str(right))
    text += """\n## Изменения по доле средств по ГРБС \n"""
    text += """\n### Значительные изменения, более чем на 50% в:\n
    """
    text += """\n
| доля | сумма изменений | ГРБС | 
| :--- | :--- | ---: |
"""
    for r in groups['great']:
        text += '| %.2f%% | %.4f млрд руб | %s | \n' % (
        round(r['share'], 2), round(r['change'] / 1000000, 4), r['name'])

    text += """\n### Существенные изменения, от 10 до 50% в:\n
    """
    text += """\n
| доля | сумма изменений | ГРБС | 
| :--- | :--- | ---: |
"""
    for r in groups['medium']:
        text += '| %.2f%% | %.4f млрд руб | %s | \n' % (
        round(r['share'], 2), round(r['change'] / 1000000, 4), r['name'])

    text += """\n### Малые изменения, до 10% в:\n
    """
    text += """\n
| доля | сумма изменений | ГРБС | 
| :--- | :--- | ---: |
"""

    for r in groups['little']:
        text += '| %.2f%% | %.4f млрд руб | %s | \n' % (
        round(r['share'], 2), round(r['change'] / 1000000, 4), r['name'])

    if not without_unchanged:
        text += """\n### Без изменений:\n
        """
        text += """\n
| ГРБС | 
| ---: |
    """
        for r in groups['nochange']:
            text += '| %s | \n' % (round(r['share'], 2), r['name'])
    else:
        text += """\nУ %d органов власти объём выделенных средств не изменился""" % (len(groups['nochange']))

    text += """\n## Абсолютные изменения по ГРБС \n"""
    text += """\n
| N | ГРБС | доля | сумма изменений | 
| ---: | :--- | ---: | ---: |
"""

    ad = ad.sort_values(by=[d_f], ascending=False)
    i = 0
    for index, r in ad.iterrows():
        i += 1
        if r[d_f] != 0:
            text += '| %d | %s | %.2f%% | %.4f млрд руб |\n' % (
            i, r['name'], round(r[ds_f], 2), round(r[d_f] / 1000000, 4))

    return text
