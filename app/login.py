from flask import Blueprint, render_template, request, flash, redirect, url_for
from start import user

login = Blueprint('login', __name__)

@login.route('/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if (user.login(username, password)):
            print('Connected')
            return redirect(url_for('decks.list'))
        # if(user.cursor.rowcount != 0):
        #     print('Connected')
        
        # print(user.cursor.rowcount)
        # print("HERE")
        # if(user.cursor.rowcount != 0):
            
        #     print()
        else:
            print("User does not exist!")
            flash("Unable to login. Please check that username and/or password are correct", category='error')
    
    #redirect(url_for('login.login_page')) # To flush the POST, so user/pass don't get resubmitted when refreshing: Doesn't seem to work
    return render_template('login.html')
    