from flask import Blueprint, render_template, flash, request, redirect

cardCollection = Blueprint('cardCollection', __name__)

@cardCollection.route('/', methods=['GET', 'POST'])
def list():
    from start import user
    userCollection = []
    results = []
    username = user.username
    print(username)
    collection = user.collection.get()

    if request.method == "POST":
        cardName = request.form['search']
        print(cardName)
        collection = user.collection.get()
        for card in collection:
            user.cursor.execute('''
                SELECT cardID, name, largeImage, types
                FROM cards
                WHERE cardID = %s AND upper(name) = upper(%s)''',
                (card, cardName))
            userCollection.append(user.cursor.fetchone())
        print(userCollection)
        for item in userCollection:
            if item is not None :
                results.append(item)    
        print(results)
        return render_template('collection.html', username=username, cards=results)
    else:
        for card in collection:
            user.cursor.execute('''
                SELECT cardID, name, largeImage, types
                FROM cards
                WHERE cardID = %s''',
                (card))
            userCollection.append(user.cursor.fetchone())
        print(userCollection)
    
        return render_template('collection.html', username=username, cards=userCollection)

@cardCollection.route('/delete/<cardID>', methods=['GET', 'POST'])
def delete(cardID):
    from start import user

    user.collection.delete(cardID)

    return redirect('/cardCollection')
