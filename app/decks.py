from flask import Blueprint, render_template
from start import user

decks = Blueprint('decks', __name__)

@decks.route('/')
def list():
    decks = user.decks.getAllDeckInfo()
    # var = ['decks.html', 'style.html']
    
    return render_template('decks.html', decks=decks)

@decks.route('/<deck_ID>')
def edit(deckID):
    # var = ['deck_edit.html', 'style.html']

    return render_template('deck_edit.html', deckID=deckID)