from flask import Flask
import psycopg2
from psycopg2 import Error
from psycopg2 import *
from user_items import *
from flask import flash
from connect import DBConnection

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'asdf'
    user = DBConnection('asdf','asdf')
    
    if(user.cursor.rowcount != 0):
        print('Connected')
    from .views import views
    from .decks import decks
    from .deckManager import deckManager
    from .login import login
    from .signUp import signUp
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(decks, url_prefix='/decks')
    app.register_blueprint(deckManager, url_prefix='/')
    app.register_blueprint(login, url_prefix='/login')
    app.register_blueprint(signUp, url_prefix='/sign_up')

    return app