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
    cardInfo = []

    if request.method == "POST":
        if request.form.get('search-collection') != None:
            conds = dict(request.form['search-collection'])
            cardInfo = user.collection.search(conds)
    else:
        cardInfo = user.collection.search({})

    #     data = dict(request.form)
    #     cardName = (data["search"])
    #     cardName += '%' # add % for LIKE functionality 
    #     print(cardName)
    #     collection = user.collection.get()
    #     for card in collection:
    #         user.cursor.execute('''
    #             SELECT cardID, name, smallImage, largeImage, types, count
    #             FROM cards
    #             WHERE cardID = %s AND upper(name) LIKE upper(%s)''',
    #             (card, cardName))
    #         userCollection.append(user.cursor.fetchone())
    #     print(userCollection)
    #     for item in userCollection:
    #         if item is not None :
    #             results.append(item)    
    #     print(results)
    #     return render_template('collection.html', user=user, cards=results)
    # else:
    #     for card in collection:
    #         user.cursor.execute('''
    #             SELECT cardID, name, smallImage, largeImage, types, count
    #             FROM cards
    #             WHERE cardID = %s''',
    #             (card))
    #         userCollection.append(user.cursor.fetchone())
    #     print(userCollection)
    
        return render_template('collection.html', user=user, cards=cardInfo)

@cardCollection.route('/delete/<cardID>', methods=['GET', 'POST'])
def delete(cardID):
    from start import user

    user.collection.delete(cardID)

    return redirect('/cardCollection')
