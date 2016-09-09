import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'pyda.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('PYDA_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

""" ROUTINGS """

@app.route('/')
def show_passwords():
    db = get_db()
    cur = db.execute('select title, username, password, website, description from passwords order by id desc')
    passwords = cur.fetchall()
    return render_template('show_passwords.html', passwords=passwords)

@app.route('/add', methods=['POST'])
def add_password():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into passwords (title, username, password, website, description) values (?, ?, ?, ?, ?)',
                 [request.form['title'], request.form['username'], request.form['password'], request.form['website'], request.form['description']])
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

" 'flask initdb' command available over cli, so no sqlite is needed "
" creates pyda.db from schema.sql "
def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

