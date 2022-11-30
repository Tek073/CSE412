from flask import Blueprint, render_template, request, flash, redirect, url_for



signUp = Blueprint('signUp', __name__)

@signUp.route('/', methods=['GET','POST'])
def signup_page(): 
    if request.method == 'POST':
        from start import user
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
    return render_template("signUp.html")