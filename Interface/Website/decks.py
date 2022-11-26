from flask import Blueprint, render_template

decks = Blueprint('decks', __name__)

@decks.route('/decks')
def home():
    var = ['help.html', 'style.html']
    
    return render_template('help.html')