from flask import Blueprint, render_template, request, flash,redirect, url_for
from connect import addUser, checkIfExists
signUp = Blueprint('signUp', __name__)

@signUp.route('/SignUp', methods=['GET','POST'])
def signUP(): 
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = checkIfExists(username, password)
        numOfResults = user.cursor.fetchone()
        user.cursor.close()
        if(numOfResults):
            flash("User with that Username ALREADY EXISTS", category='error')
            print()
        else:
            user = addUser(username, password)
            user.cursor.close()
            return redirect(url_for('decks.home'))
    return render_template("signUp.html")