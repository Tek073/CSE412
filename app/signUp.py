from flask import Blueprint, render_template, request, flash
from start import user


signUp = Blueprint('signUp', __name__)

@signUp.route('/', methods=['GET','POST'])
def signUP(): 
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if (user.signup(username, password)):
            print('Registered')
        # if(user.cursor.rowcount != 0):
        #     print('Connected')
        
        # print(user.cursor.rowcount)
        # print("HERE")
        # if(user.cursor.rowcount != 0):
            
        #     print()
        else:
            print("Username taken!")
            flash("Cannot register account: Username taken", category='error')

    return render_template("signUp.html")