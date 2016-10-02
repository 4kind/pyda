from flask import render_template, flash, redirect, url_for
from flask_login import current_app
from . import main
from ..models import User, Role
from .. import db
from ..auth.forms import CreateUserForm


@main.route('/', methods=['GET', 'POST'])
def index():
    number_admins = User.query.filter(User.role.has(name='Administrator')).count()  #
    admin_role = Role.query.filter_by(name='Administrator').first()
    if admin_role is not None and number_admins == 0:
        form = CreateUserForm()
        if form.validate_on_submit():
            u = User()
            form.populate_obj(u)
            u.role = admin_role
            db.session.add(u)
            flash('Admin User was created.')
            return redirect(url_for('auth.login'))
        form.email.data = current_app.config['PYDA_ADMIN']
        return render_template("auth/create_admin.html", form=form)
    return render_template('index.html')
