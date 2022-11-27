from flask import Blueprint, render_template, request, flash, redirect, url_for
from start import user

login = Blueprint('login', __name__)

@login.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if (user.login(username, password)):
            print('Connected')
        # if(user.cursor.rowcount != 0):
        #     print('Connected')
        
        # print(user.cursor.rowcount)
        # print("HERE")
        # if(user.cursor.rowcount != 0):
            
        #     print()
        else:
            print("User does not exist!")
            flash("Unable to login. Please check that username and/or password are correct", category='error')
    
    return render_template('login.html')