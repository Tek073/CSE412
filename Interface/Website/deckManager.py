from flask import Blueprint, render_template

deckManager = Blueprint('deckManager', __name__)

@deckManager.route('/deckManager')
def home():
    var = ['navbar.html', 'style.html']
    
    return "<h1>Deck Manager</h1>"