# -*- coding: utf-8 -*-
import xlwt

from .extract import get_full_budget_data
from .diff import grbs_date_diff, programs_date_diff, vr_date_diff, projects_date_diff, full_date_diff

REPORT_PARTS = {'svod' : 'Сводные данные',
                'grbs_rel': "По ГРБС относительно",
                'grbs_abs' : "По ГРБС абсолютно",
                'programs' : "По госпрограммам",
                'vr' : 'По видам расходов',
                'projects' : 'По нацпроектам',
                'changes' : 'Все изменения'}


def write_sheet_item(sheet, rowid, item):
    i = 0
    for v in item:
        sheet.write(rowid, i, v)
        i += 1

def write_sheet_items(sheet, startrow, keyvalues):
    for i in range(0, len(keyvalues), 1):
        write_sheet_item(sheet, i + startrow, keyvalues[i])


def report_diff_excel(filename, left_date, right_date, parts=['grbs_rel', 'grbs_abs', 'programs','projects', 'changes'], original=True):
    """Создает Excel отчёт об изменениях в сводной бюджетной росписи между двумя датами."""
    wb = xlwt.Workbook()
    print('1. Собираются данные по датам')
    frames = [get_full_budget_data(left_date), get_full_budget_data(right_date)]
    sh_svod = wb.add_sheet(REPORT_PARTS['svod'])
    sh_svod.write(0, 0, 'Изменения в сводной бюджетной росписи с %s по %s' % (str(left_date), str(right_date)))

    print('2. Формируется таблица сравнения по ГРБС')
    grbs_difftable = grbs_date_diff([left_date, right_date], frames=frames)
    left_f = str(left_date).replace('.', '_')
    right_f = str(right_date).replace('.', '_')
    ds_f = str(right_date).replace('.', '_') + '_ds'
    d_f = str(right_date).replace('.', '_') + '_d'

    left_sum = grbs_difftable[left_f].sum()
    right_sum = grbs_difftable[right_f].sum()
    keyvalues = [
        ['Итого на %s' % str(left_date), left_sum],
        ['Итого на %s' % str(right_date), right_sum],
        ['Сумма изменений', right_sum - left_sum],
        ['Доля изменений', round(100*(right_sum - left_sum) / left_sum, 4)],
        ['Всего ГРБС', len(grbs_difftable)],
        ['ГРБС с изменениями', len(grbs_difftable[grbs_difftable[d_f] != 0])]
    ]

    if 'grbs_rel' in parts or 'grbs_abs' in parts:
        if 'grbs_rel' in parts:
            sh_grbs_rel = wb.add_sheet(REPORT_PARTS['grbs_rel'])
            header = ['начальная сумма', 'итоговая сумма', 'сумма изменений', 'доля', 'ГРБС' ]
            for column, heading in enumerate(header):
                sh_grbs_rel.write(0, column, heading)

            ad = grbs_difftable.sort_values(by=ds_f, ascending=False)
            dname = str(right_date).replace('.', '_')
            i = 0
            for index, r in ad.iterrows():
                i += 1
                if r[d_f] != 0:
                    sh_grbs_rel.write(i, 0, round(r[left_f], 4))
                    sh_grbs_rel.write(i, 1, round(r[dname], 4))
                    sh_grbs_rel.write(i, 2, round(r[dname+ '_d'], 4))
                    sh_grbs_rel.write(i, 3, round(r[dname+'_ds'], 4))
                    sh_grbs_rel.write(i, 4, r['name'])


        if 'grbs_abs' in parts:
            sh_grbs_abs = wb.add_sheet(REPORT_PARTS['grbs_abs'])
            header = ['начальная сумма', 'итоговая сумма', 'сумма изменений', 'доля', 'ГРБС' ]
            for column, heading in enumerate(header):
                sh_grbs_abs.write(0, column, heading)

            ad = ad.sort_values(by=[d_f], ascending=False)
            i = 0
            for index, r in ad.iterrows():
                i += 1
                if r[d_f] != 0:
                    sh_grbs_abs.write(i, 0, round(r[left_f], 4))
                    sh_grbs_abs.write(i, 1, round(r[dname], 4))
                    sh_grbs_abs.write(i, 2, round(r[dname+ '_d'], 4))
                    sh_grbs_abs.write(i, 3, round(r[dname+'_ds'], 4))
                    sh_grbs_abs.write(i, 4, r['name'])

    print('3. Формируется таблица сравнения по госпрограммам')
    prg_difftable = programs_date_diff([left_date, right_date], frames=frames)
    prg_total = len(prg_difftable)
    prg_changed = len(prg_difftable[prg_difftable[d_f] != 0])
    keyvalues.append(['Госпрограмм всего', prg_total])
    keyvalues.append(['Госпрограмм изменено', prg_changed])

    if 'programs' in parts:
        sh_prg = wb.add_sheet(REPORT_PARTS['programs'])
        header = ['код программы', 'название', 'сумма на %s' % (str(left_date)), 'сумма на %s' % (str(right_date)),
                  'сумма изменений', 'доля']
        for column, heading in enumerate(header):
            sh_prg.write(0, column, heading)

        ad = prg_difftable.sort_values(by=ds_f, ascending=False)
        keys = ['program', 'name', left_f, right_f, d_f, ds_f]
        i = 0
        for index, r in ad.iterrows():
            i += 1
            n = 0
            for k in keys:
                sh_prg.write(i, n, r[k] if r[k] is not None else '')
                n += 1

    print('3.1. Формируется таблица сравнения по нацпроектам')
    proj_difftable = projects_date_diff([left_date, right_date], frames=frames)
    proj_total = len(proj_difftable)
    proj_changed = len(proj_difftable[proj_difftable[d_f] != 0])
    keyvalues.append(['Нацпроектов всего', proj_total])
    keyvalues.append(['нацпроектов изменено', proj_changed])

    if 'projects' in parts:
        sh_proj = wb.add_sheet(REPORT_PARTS['projects'])
        header = ['код нацпроекта', 'название', 'сумма на %s' % (str(left_date)), 'сумма на %s' % (str(right_date)),
                  'сумма изменений', 'доля']
        for column, heading in enumerate(header):
            sh_proj.write(0, column, heading)

        ad = proj_difftable.sort_values(by=ds_f, ascending=False)
        keys = ['project', 'name', left_f, right_f, d_f, ds_f]
        i = 0
        for index, r in ad.iterrows():
            i += 1
            n = 0
            for k in keys:
                sh_proj.write(i, n, r[k] if r[k] is not None else '')
                n += 1


    print('4. Формируется таблица сравнения по видам расходов')
    vr_difftable = vr_date_diff([left_date, right_date], frames=frames)
    vr_total = len(vr_difftable)
    vr_changed = len(vr_difftable[vr_difftable[d_f] != 0])
    keyvalues.append(['Видов расходов всего', vr_total])
    keyvalues.append(['Видов расходов изменено', vr_changed])

    if 'vr' in parts:
        sh_vr = wb.add_sheet(REPORT_PARTS['vr'])
        header = ['код вида расхрдов', 'название', 'сумма на %s' % (str(left_date)), 'сумма на %s' % (str(right_date)),
                  'сумма изменений', 'доля']
        for column, heading in enumerate(header):
            sh_vr.write(0, column, heading)

        ad = vr_difftable.sort_values(by=ds_f, ascending=False)
        keys = ['vr', 'name', left_f, right_f, d_f, ds_f]
        i = 0
        for index, r in ad.iterrows():
            i += 1
            n = 0
            for k in keys:
                sh_vr.write(i, n, r[k] if r[k] is not None else '')
                n += 1

    print('5. Идёт расчёт таблицы полных отличий СБР')
    fulldiff = full_date_diff(left_date, right_date, frames=frames)
    keyvalues.append(['Всего изменено строк', len(fulldiff)])
    keyvalues.append(['Содержательно изменённые строки', len(fulldiff[fulldiff['vr'].isnull() == False]),
                      'Изменения затрагивающие только строки с видами расходов (остальные строки меняются автоматически по иерархии)'])
    if 'changes' in parts:
        sh_changes = wb.add_sheet(REPORT_PARTS['changes'])
        header = ['статус', 'сумма изменений', 'доля', 'название', 'ГРБС', 'раздел', 'подраздел',
                  'программная (непрограммная) статья расходов', 'статья расходов', 'вид расходов', 'сумма']
        for column, heading in enumerate(header):
            sh_changes.write(0, column, heading)

        i = 0
        keys = ['status', 'change', 'change_share', 'name', 'grbs', 'topic', 'subtopic', 'csr_program', 'csr_article',
                'vr', 'budget2019']
        for index, r in fulldiff.iterrows():
            i += 1
            n = 0
            for k in keys:
                sh_changes.write(i, n, r[k] if r[k] is not None else '')
                n += 1

    write_sheet_items(sh_svod, startrow=2, keyvalues=keyvalues)

    print('6. Формируется итоговый отчёт')
    wb.save(filename)


