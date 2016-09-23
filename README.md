# pyda

## installation
1. git clone https://github.com/basspencer/pyda
2. cd pyda
3. virtualenv venv
4. source venv/bin/activate
5. pip install flask flask-script flask-sqlalchemy

## start developing
1. export FLASK_APP=pyda.py
2. export FLASK_DEBUG=1

## create database
1. python pyda.py shell
2. >> from pyda import db
3. >> db.create_all()

## run server
1. python pyda.py runserver -h 127.0.0.1