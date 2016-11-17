import sqlite3
import csv


# Read csv file
with open('./members.csv', newline='') as csv_file:
    rows = csv.DictReader(csv_file)
    members = [(row['名字'], row['團體']) for row in rows]

# Print csv
# print(members)

# read create db file
with open('./create_db.sql', 'r') as sql_file:
    create_db_sql = sql_file.read()

# Connect to db
db = sqlite3.connect('members.db')

# Inset csv to db
with db:
    db.executescript(create_db_sql)
    db.executemany('INSERT INTO  members (name, group_name) VALUES (?, ?)',
                   members)

# Print db
"""
connection = db.execute('SELECT * FROM members LIMIT 3')
for data in connection:
    print(data)
"""
