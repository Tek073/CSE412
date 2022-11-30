from flask import Blueprint, render_template, flash, request, redirect
from globals import search_cards

addToCollection = Blueprint('addToCollection', __name__)

@addToCollection.route('/', methods=['GET', 'POST'])
def begin():
    from start import user
    userCollection = []
    results = []
    username = user.username
    print(username)
    collection = user.collection.get()


    return render_template('addToCollection.html')

@addToCollection.route('/add/<cardID>', methods=['GET', 'POST'])
def add(cardID):
    from start import user

    user.cursor.execute('''
        INSERT INTO _cards_in_collections VALUES
        (%s, %s, %s)''',
        (user.id, cardID, 1))
    user.conn.commit()

    return redirect('/addToCollection')

@addToCollection.route('/search', methods=['GET', 'POST'])
def search(): 
    from start import user
    userCollection = []
    if request.method == "POST":
        cardName = request.form['cardName']
        print(cardName)
        user.cursor.execute('''
            SELECT cardID, name, largeImage, types
            FROM cards
            WHERE upper(name) LIKE upper(%s)''',
            [cardName])
        
        for card in user.cursor.fetchall():
            userCollection.append(card)
        print(userCollection)
    return render_template('addToCollection.html', username=user.username, cards=userCollection)
    