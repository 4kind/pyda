import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, 'pyda.db')
SECRET_KEY='development key'
USERNAME='admin'
PASSWORD='default'