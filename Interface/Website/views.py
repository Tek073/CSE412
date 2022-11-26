from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    var = ['navbar.html', 'style.html']
    
    return render_template(var)