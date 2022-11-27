from flask import Blueprint,Flask, render_template, request, flash, redirect, url_for
from connect import DBConnection


login = Blueprint('login', __name__)

@login.route('/Login', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = DBConnection(username, password)
        if(user.cursor.rowcount != 0):
            print('Connected')
        
        print(user.cursor.rowcount)
        print("HERE")
        if(user.cursor.rowcount != 0):
            return redirect(url_for('decks.home'))
        else:
            print("User Dont Exist")
            flash("Check Username and/or Password", category='error')
            
        
    
    return render_template('login.html')