from flask import Blueprint, render_template, request
from start import user

settings = Blueprint('settings', __name__)

@settings.route('/', methods=['GET', 'POST'])
def home():
    var = ['navbar.html', 'style.html']
    if (request.method == 'POST'):
        print (request.form)
        if request.form.get('toggle_loadimages') != None \
        and request.form.get('toggle_loadimages') == 'on':
            user.loadimages = True
        else:
            user.loadimages = False

    return render_template('settings.html', user=user)