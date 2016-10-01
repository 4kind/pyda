from flask import render_template, redirect, flash, url_for, request
from flask_login import login_required
from . import passwords
from .. import db
from ..models import Password
from .forms import PasswordForm


@passwords.route('/show-passwords')
@login_required
def show_passwords():
    passwords_all = Password.query.all()
    return render_template('passwords/show_passwords.html', passwords=passwords_all)


@passwords.route('/add-password', methods=['GET', 'POST'])
@login_required
def add_password():
    form = PasswordForm()
    if form.validate_on_submit():
        p = Password()
        form.populate_obj(p)
        db.session.add(p)
        flash('Your password has been added.')
        return redirect(url_for('passwords.show_passwords'))
    return render_template("passwords/add_password.html", form=form)


@passwords.route('/edit-password', methods=['GET', 'POST'])
@login_required
def edit_password():
    p = Password.query.get_or_404(request.args.get('id'))
    form = PasswordForm(obj=p)

    if p is not None:
        if form.validate_on_submit():
            form.populate_obj(p)
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('passwords.show_passwords'))
    else:
        flash('The Password does not exist.')
        return redirect(url_for('passwords.show_passwords'))
    return render_template("passwords/edit_password.html", form=form)


@passwords.route('/delete-password', methods=['GET', 'POST'])
@login_required
def delete_password():
    p = Password.query.get_or_404(request.args.get('id'))
    if p is not None:
        db.session.delete(p)
        db.session.commit()
    else:
        flash('The Password does not exist.')
    return redirect(url_for('passwords.show_passwords'))
