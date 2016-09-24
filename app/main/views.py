from datetime import datetime
from flask import render_template, session, redirect, url_for, abort, flash, request
from . import main
from .forms import NameForm
from .. import db
from ..models import Password


@main.route('/')
def show_passwords():
    passwords = Password.query.all()
    return render_template('show_passwords.html', passwords=passwords)


@main.route('/add', methods=['POST'])
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
    return redirect(url_for('.show_passwords'))


@main.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin':
            error = 'Invalid username'
        elif request.form['password'] != 'default':
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('.show_passwords'))
    return render_template('login.html', error=error)


@main.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('.show_passwords'))
