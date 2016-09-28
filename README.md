# pyda

## installation
1. git clone https://github.com/basspencer/pyda
2. cd pyda
3. virtualenv venv
4. source venv/bin/activate
5. pip install -r requirements.txt

## create database
* python manage.py db upgrade

## create admin user
*  python manage.py create_user <email> <usernam> <password>

## run server
* python manage.py runserver

## run tests
* python manage.py test