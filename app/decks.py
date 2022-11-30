from flask import Blueprint, redirect, render_template, request, url_for

from start import user
from globals import search_cards

cur = user.cursor
deck = user.decks
cardInfo = []

decks = Blueprint('decks', __name__)

@decks.route('/decks')
def list():
    from start import user

    cur = user.cursor
    deck = user.decks
    cardInfo = []
    decks = user.decks.getInfoFromAllDecks()
    return render_template('decks.html', user=user, decks=decks)

# Edit one specific deck. 
# NOTE: updates deckID
@decks.route('/decks/<deckID>', methods=['GET', 'POST'])
def edit(deckID):
    from start import user

    cur = user.cursor
    deck = user.decks
    cardInfo = []
    user.decks.changeTo(deckID) 

    if request.method == 'POST':
        data = dict(request.form)
        temp = dict(data) # create copy of data, so we can delete key-value pairs during iteration
        for key in temp:
            if temp[key] == '':
                del data[key]
        print(data)
        w = ' AND '.join(cur.mogrify('%s = %%s' % key, [data[key]]).decode() for key in data)
        print(w)
        
        if data.get('search-collectiona') != None:
            del data['search-collection']
            user.collection.search(data)
        if data.get('search-deck') != None:
            del data['search-deck']
            user.decks.search(data)

    cur.execute('''
        SELECT c.cardID, c.name, count, largeImage
        FROM _cards_in_decks cic, cards c
        WHERE userID = %s
        AND deckID = %s
        AND cic.cardID = c.cardID''',
        (user.id, deckID))

    cardInfo = cur.fetchall()

    deck = user.decks
    deckID = deck.deckID
    return render_template('deck_edit.html', user=user, deck=deck, cardInfo=cardInfo)

# See detailed card info for one card. Also can delete a card
@decks.route('/decks/<deckID>/<cardID>', methods=['GET', 'POST'])
def card_edit(deckID, cardID):
    from start import user

    cur = user.cursor
    deck = user.decks
    cardInfo = []
    if request.method == 'POST':
        if request.form.get('del-card') == 'del-card':
            user.decks.delete(deckID, cardID)
            return redirect(url_for('decks.edit', deckID=deckID))

    return render_template('card_edit.html', deckID=deckID, cardID=cardID, cardInfo=cardInfo)