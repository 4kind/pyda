from flask_script import Manager
from flask import Flask, request, session, redirect, url_for, abort, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('settings')
app.config.from_envvar('PYDA_SETTINGS', silent=True)

db = SQLAlchemy(app)

manager = Manager(app)

""" MODELS """


class Password(db.Model):
    __tablename__ = 'passwords'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True, nullable=False, unique=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    website = db.Column(db.String(100))
    description = db.Column(db.String(200))

    def __repr__(self):
        return '<Password %r>' % self.title


"""
ROUTINGS 
"""


@app.route('/')
def show_passwords():
    passwords = Password.query.all()
    return render_template('show_passwords.html', passwords=passwords)


@app.route('/add', methods=['POST'])
def add_password():
    if not session.get('logged_in'):
        abort(401)
    password = Password(
        title=request.form['title'],
        username=request.form['username'],
        password=request.form['password'],
        website=request.form['website'],
        description=request.form['description'],
    )
    db.session.add(password)
    db.session.commit()
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


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    manager.run()
