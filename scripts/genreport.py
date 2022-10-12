import os
import datetime
from budgetlib.report import report_diff_excel
from budgetlib.views import programs_view, vr_view, projects_view, grbs_view, grbs_vr_view
from budgetlib.extract import get_full_budget_data

def sample_view():
    adate = datetime.date(2019, 6, 1)
    ad = get_full_budget_data(adate)
    d = grbs_vr_view(adate, frame=ad)
    print(d[['name', '100', '200']])

def generate_reports():
    files = os.listdir('data/raw')
    files.sort()
    i = 1
    print(files)
    for i in range(1, len(files)):
        d2 = datetime.date(*map(int, files[i].rsplit('.', )[0].split('-')))
        d1 = datetime.date(*map(int, files[i-1].rsplit('.', )[0].split('-')))
        print(d1, d2)
        filename = 'reports/report_%s_%s.xls' % (files[i-1].rsplit('.', 1)[0].replace('-', ''), files[i].rsplit('.', 1)[0].replace('-', ''))
        if not os.path.exists(filename):
            report_diff_excel(filename, left_date=d1, right_date=d2, parts=['svod', 'grbs_rel', 'grbs_abs', 'projects', 'programs', 'vr', 'changes'])

if __name__ == "__main__":
#    sample_view()
    generate_reports()

