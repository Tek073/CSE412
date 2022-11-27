from flask import Blueprint, render_template
from Interface.__init__ import *

decks = Blueprint('decks', __name__)

@decks.route('/')
def home():
    decks = user.decks.getAllDeckInfo()
    var = ['decks.html', 'style.html']
    
    return render_template('decks.html', )

@decks.route('/<deck_ID>')
def edit():
    var = ['deck_edit.html', 'style.html']