import csv


with open('../db/members.csv', newline='') as csv_file:
    rows = csv.DictReader(csv_file)
    for row in rows:
        print('{0} of {1}'.format(row['名字'], row['團體']))
