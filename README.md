# BudgetLib

Библиотека для языка Python по преобразованию данных сводной бюджетной росписи в срезы для последующего анализа и визуализации
Библиотека сейчас использует только данные с budget.gov.ru через API сводной бюджетной росписи и заточено под данные за 2019 год

# Требования к работе

Прежде чем начать работать с кодом необходимо, либо скачать и распаковать из архива, или 
закешировать с сайта budget.gov.ru бюджетную роспись начиная с января 2019 год. 

Это делается через функцию budgetlib.collect.save_all(filepath) где filepath по умолчанию в папке 
'data/raw'

# Код

Функция "get_full_budget_data" возвращает данные сводной росписи на дату в формате pandas DataFrame
    >>> from budgetlib.extract import get_full_budget_data
    >>> frame = get_full_budget_data(datetime.date(2019, 6, 1))
    возвращает сводную роспись на указанную дату

    >>> from budgetlib.view import project_view
    >>> projects = projects_view(datetime.date(2019, 6, 1), frame=frame)
    Возвращает список проектов в бюджетной росписи и выделенные на них суммы. Если задан параметр frame то вместо загрузки данных из закешированных CSV использует данные из frame

    >>> from budgetlib.diff import grbs_date_diff
    >>> dates = [datetime.date(2019, 6, 1), datetime.date(2019, 6, 2)]
    >>> grbs_diff = grbs_date_diff(dates)
    подгружает сводные росписи на 2 или большее число дат и на их основе строит таблицу изменений

    >>> from budgetlib.diff import full_date_diff
    >>> full_date_diff = full_date_diff(datetime.date(2019, 6, 1), datetime.date(2019, 6, 2))
    строит таблицу построчного сравнения и изменений в сводных бюджетных росписях между двумя датами
    
    >>> from budgetlib.report import report_diff_excel
    >>> d1 = datetime.date(2019, 6, 1)
    >>> d2 = datetime.date(2019, 6, 2)
    >>> report_diff_excel("report_1-2_6_2019.xls", left_date=d1, right_date=d2, parts=['svod', 'grbs_rel', 'grbs_abs', 'projects', 'programs', 'vr', 'changes'])
    создаёт файл отчёта в Excel с разделами: по ГРБС относительно, по ГРБС абсолютно, по госпрограммам, по национальным проектам, по видам расходов и таблица изменений

# Требования

* xlwt https://github.com/python-excel/xlwt
* pandas https://pandas.pydata.org/


# TODO
* добавить универсальности поддержки любого года, не только 2019
* добавить учёт будущих лет в росписи
* добавить подгрузку данных о кассовом исполнении
* добавить блок с примерами

# Авторы

Иван Бегтин (ivan@begtin.tech)
