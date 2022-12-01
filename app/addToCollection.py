from flask import Blueprint, render_template, flash, request, redirect
from globals import search_cards

addToCollection = Blueprint('addToCollection', __name__)

@addToCollection.context_processor
def utility_functions():
    def print_in_console(message):
        print (message)

    return dict(mdebug=print_in_console)

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

    user.collection.add(cardID)
    # user.cursor.execute('''
    #     INSERT INTO _cards_in_collections VALUES
    #     (%s, %s, %s)''',
    #     (user.id, cardID, 1))
    # user.conn.commit()

    return redirect('/addToCollection')

@addToCollection.route('/search', methods=['GET', 'POST'])
def search(): 
    from start import user
    cardsToAdd = []
    collection = []
    if request.method == "POST":
        cardName = request.form['cardName']
        cardName += '%'
        print(cardName)
        user.cursor.execute('''
            SELECT cardID, name, smallImage, largeImage, types
            FROM cards
            WHERE upper(name) LIKE upper(%s)''',
            [cardName])
        
        collection = user.cursor.fetchall()
        for card in collection:
            cardsToAdd.append(card)
        print(cardsToAdd)
    return render_template('addToCollection.html', user=user, cards=cardsToAdd)
    