from flask import Blueprint, render_template

signUp = Blueprint('signUp', __name__)

@signUp.route('/SignUp')
def home(): 
    return render_template('signUp.html')