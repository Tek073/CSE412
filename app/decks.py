from flask import Blueprint, render_template
from start import user

decks = Blueprint('decks', __name__)

@decks.route('/')
def list():

    #if (user.id != 0):
    username = user.username
    decks = user.decks.getAllDeckInfo()
    # var = ['decks.html', 'style.html']
    
    return render_template('decks.html', username=username, decks=decks)

@decks.route('/<deck_ID>')
def edit(deckID):
    # var = ['deck_edit.html', 'style.html']

    return render_template('deck_edit.html', deckID=deckID)