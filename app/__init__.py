from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'asdf'

    from .views import views
    from .decks import decks
    from .deckManager import deckManager
    from .login import login
    from .signup import signup
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(decks, url_prefix='/decks')
    app.register_blueprint(deckManager, url_prefix='/')
    app.register_blueprint(login, url_prefix='/login')
    app.register_blueprint(signup, url_prefix='/sign_up')

    return app