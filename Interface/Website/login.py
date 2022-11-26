from flask import Blueprint, render_template

login = Blueprint('login', __name__)

@login.route('/Login')
def home():
    var = ['help.html', 'style.html']
    
    return render_template('help.html')