from flask import render_template, redirect, flash, url_for, request
from . import passwords
from .. import db
from ..models import Password, Permission
from .forms import PasswordForm
from ..decorators import permission_required


@passwords.route('/show-passwords')
@permission_required(Permission.READ)
def show_passwords():
    passwords_all = Password.query.all()
    return render_template('passwords/show_passwords.html', passwords=passwords_all)


@passwords.route('/add-password', methods=['GET', 'POST'])
@permission_required(Permission.WRITE)
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
@permission_required(Permission.WRITE)
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


@passwords.route('/delete-password')
@permission_required(Permission.WRITE)
def delete_password():
    p = Password.query.get_or_404(request.args.get('id'))
    if p is not None:
        if request.args.get('confirm') == '1':
            db.session.delete(p)
            db.session.commit()
            flash('Your password has been deleted.')
        else:
            flash({p.id: 'Do you want to delete this password?'}, 'confirm')
    return redirect(url_for('passwords.show_passwords'))
