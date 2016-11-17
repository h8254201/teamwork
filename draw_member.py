import csv
import sqlite3
import random
from flask import Flask, g, render_template, request
from datetime import datetime


app = Flask(__name__)
SQLITE_DB_PATH = 'db/members.db'
SQLITE_DB_SCHEMA = 'db/create_db.sql'
MEMBER_CSV_PATH = 'db/members.csv'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/draw', methods=['POST'])
def draw():
    db = get_db()
    group_name = request.form.get('group_name', 'ALL')
    valid_members_sql = 'SELECT id FROM members '

    if group_name == 'ALL':
        cursor = db.execute(valid_members_sql)
    else:
        valid_members_sql += 'WHERE group_name = ?'
        cursor = db.execute(valid_members_sql, (group_name, ))

    valid_member_ids = [row[0] for row in cursor]

    if not valid_member_ids:
        err_msg = '<p>No members in group {0}</p>'.format(group_name)
        return err_msg, 404

    lucky_member_id = random.choice(valid_member_ids)
    sql = 'SELECT name, group_name FROM members WHERE id = ?'
    member_name, member_group_name = db.execute(sql,
                                                (lucky_member_id, )).fetchone()

    with db:
        db.execute('INSERT INTO draw_histories (memberid) VALUES (?)',
                   (lucky_member_id, ))

    return render_template('draw.html',
                           name=member_name,
                           group=member_group_name)


@app.route('/history')
def history():
    db = get_db()
    c = db.execute('SELECT m.name, m.group_name, d.time AS "draw_time [timestamp]" '
                   'FROM draw_histories AS d, members AS m '
                   'WHERE m.id == d.memberid '
                   'ORDER BY d.time DESC '
                   'LIMIT 10').fetchall()

    recent_histories = []
    for row in c:
        recent_histories.append({'name': row[0],
                                 'group': row[1],
                                 'draw_time': datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')})

    return render_template('history.html',
                           recent_histories=recent_histories)


# db setting
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(SQLITE_DB_PATH)
        db.execute('PRAGMA foreign_keys = ON')

    return db


# close db connect
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run(debug=True)
