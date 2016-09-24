from flask import render_template, session, redirect, url_for, abort, flash, request
from . import passwords
from .. import db
from ..models import Password


@passwords.route('/passwords')
def show_passwords():
    passwords_all = Password.query.all()
    return render_template('passwords/show_passwords.html', passwords=passwords_all)


@passwords.route('/passwords/add', methods=['POST'])
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
    return redirect(url_for('passwords.show_passwords'))
