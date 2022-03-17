import csv
import ast


def add_ad_link():
    with open('/Users/midhatsibonjic/django_celery_results_taskresult_2.csv', 'r') as read_file, open('/Users/midhatsibonjic/django_celery_results_taskresult_3.csv', 'w') as write_file:
        csvreader = csv.reader(read_file)
        csvwriter = csv.writer(write_file)
        for row in csvreader:
            kwargs = ast.literal_eval(ast.literal_eval(row[10]))
            ad_link = kwargs.get('ad_link')
            row[14] = ad_link
            csvwriter.writerow(row)


if __name__ == '__main__':
    add_ad_link()
