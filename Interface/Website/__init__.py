from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'asdf'
    from .views import views
    from .decks import decks
    from .deckManager import deckManager
    from .login import login
    from .signUp import signUp
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(decks, url_prefix='/')
    app.register_blueprint(deckManager, url_prefix='/')
    app.register_blueprint(login, url_prefix='/')
    app.register_blueprint(signUp, url_prefix='/')

    return app