import database
from flask_script import Manager
from flask import Flask, request, session, redirect, url_for, abort, render_template, flash

app = Flask(__name__)
app.config.from_object('settings')
app.config.from_envvar('PYDA_SETTINGS', silent=True)

" create database istance "
dbs = database.Database(app)

manager = Manager(app)

"""
ROUTINGS 
"""


@app.route('/')
def show_passwords():
    db = dbs.get_db()
    cur = db.execute('select title, username, password, website, description from passwords order by id desc')
    passwords = cur.fetchall()
    return render_template('show_passwords.html', passwords=passwords)


@app.route('/add', methods=['POST'])
def add_password():
    if not session.get('logged_in'):
        abort(401)
    db = dbs.get_db()
    db.execute('insert into passwords (title, username, password, website, description) values (?, ?, ?, ?, ?)',
               [request.form['title'], request.form['username'], request.form['password'], request.form['website'],
                request.form['description']])
    db.commit()
    flash('New Password was successfully posted')
    return redirect(url_for('show_passwords'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_passwords'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_passwords'))


if __name__ == '__main__':
    manager.run()
