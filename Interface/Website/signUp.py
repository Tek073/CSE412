from flask import Blueprint, render_template, request, flash
from connect import addUser

signUp = Blueprint('signUp', __name__)

@signUp.route('/SignUp', methods=['GET','POST'])
def signUP(): 
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = addUser(username, password)
        if(user.cursor.rowcount != 0):
            print('Connected')
        
        print(user.cursor.rowcount)
        print("HERE")
        if(user.cursor.rowcount != 0):
            
            print()
        else:
            print("User Dont Exist")
            flash("Check Username and/or Password", category='error')

    return render_template("signUp.html")