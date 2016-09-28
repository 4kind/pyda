#!/usr/bin/env python
import os
from app import create_app, db
from app.models import Password, User
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, Password=Password, User=User)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """ run the unit tests """
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
@manager.option('-e', '--email', dest='email', default=None)
@manager.option('-u', '--username', dest='username', default=None)
@manager.option('-p', '--password', dest='password', default=None)
def create_user(email, username, password):
    """ create default user """
    user = User.query.filter_by(email=email).first()
    if user is not None:
        print('E-Mail already exists.')
    else:
        user = User.query.filter_by(username=username).first()
        if user is not None:
            print('Username already exists.')
        else:
            u = User()
            u.email = email
            u.username = username
            u.password = password
            db.session.add(u)
            db.session.commit()


if __name__ == '__main__':
    manager.run()
