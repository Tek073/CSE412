from flask import Flask
#from start import user

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'asdf'

    from .settings import settings
    from .decks import decks
    #from .deckManager import deckManager
    from .login import login
    from .signUp import signUp
    from .cardCollection import cardCollection
    from .addToCollection import addToCollection
    app.register_blueprint(settings, url_prefix='/')
    app.register_blueprint(decks, url_prefix='/')
    #app.register_blueprint(deckManager, url_prefix='/')
    app.register_blueprint(login, url_prefix='/login')
    app.register_blueprint(signUp, url_prefix='/sign_up')
    app.register_blueprint(cardCollection, url_prefix='/cardCollection')
    app.register_blueprint(addToCollection, url_prefix='/addToCollection')

    return app