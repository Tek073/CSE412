from flask import Blueprint, render_template, request, flash, redirect, url_for
from start import user


signup = Blueprint('signup', __name__)

@signup.route('/', methods=['GET','POST'])
def signup_page(): 
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if (user.signup(username, password)):
            user.login(username, password)
            print('Registered')
            return redirect(url_for('decks.list'))
        # if(user.cursor.rowcount != 0):
        #     print('Connected')
        
        # print(user.cursor.rowcount)
        # print("HERE")
        # if(user.cursor.rowcount != 0):
            
        #     print()
        else:
            print("Username taken!")
            flash("Cannot register account: Username taken", category='error')
            
    return render_template("signup.html")