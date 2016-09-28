from flask import render_template, session, redirect, url_for, flash, request
from . import main


@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')
