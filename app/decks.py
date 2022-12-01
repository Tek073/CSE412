from collections import Counter
from flask import Blueprint, redirect, render_template, request, url_for

from start import user
from globals import search_cards

cur = user.cursor
deck = user.decks
cardInfo = []
typeInfo = []

decks = Blueprint('decks', __name__)

@decks.route('/decks', methods=['GET','POST'])
def list():
    if request.method == 'POST':
        
        if request.form.get('deckname'):
            name = request.form['deckname']
            print(name)
            user.decks.create(name)

    decks = user.decks.getInfoFromAllDecks()
    return render_template('decks.html', user=user, decks=decks)

# Edit one specific deck. 
# NOTE: updates deckID
@decks.route('/decks/<deckID>', methods=['GET', 'POST'])
def edit(deckID):
    editable = 'deck'
    user.decks.changeTo(deckID)
    # Deck Search 
    if request.method == 'POST':
        data = dict(request.form)
        print(data)
        
        if data.get('search-collection') != None:
            print('searching collection...')
            del data['search-collection']
            print(data)
            cardInfo = user.collection.search(data)
            editable = 'collection'
        if data.get('search-decks') != None:
            print('searching deck...')
            del data['search-decks']
            print(data)
            cardInfo = user.decks.search(data)
            editable = 'no'
        if data.get('search-current-deck') != None:
            print('searching current deck...')
            del data['search-current-deck']
            print(data)
            cardInfo = user.decks.search(data, deckID=deckID)
            editable = 'deck'

    else:
        cur.execute('''
            SELECT c.cardID, c.name, smallImage, largeImage, types, count
            FROM _cards_in_decks cic, cards c
            WHERE userID = %s
            AND deckID = %s
            AND cic.cardID = c.cardID''',
            (user.id, deckID))
        cardInfo = cur.fetchall()

    cur.execute('''
    SELECT w.type, w.value, r.type, r.value
    FROM weaknesses w, resistances r, _cards_in_decks cid
    WHERE userID = %s
    AND deckID = %s
    AND w.cardID = cid.cardID AND r.cardID = cid.cardID''',
    (user.id, deckID))
    typeInfo = cur.fetchall()
    print(typeInfo)

    wkInfo = {}
    resInfo = {}
    wkTypes = {}
    wkValues = {}
    resTypes = {}
    resValues = {}
    
    for wt, wv, rt, rv in typeInfo:
        if wkTypes.get(wt) == None:
            wkTypes[wt] = 1
        else:
            wkTypes[wt] += 1
        if resTypes.get(rt) == None:
            resTypes[rt] = 1
        else:
            resTypes[rt] += 1

    # print('wt',wkTypes)
    # print('rt',resTypes)

    deck = user.decks
    deckID = deck.deckID
    return render_template('deck_edit.html', user=user, deck=deck, cardInfo=cardInfo, typeInfo=typeInfo, editable=editable)

@decks.route('/decks/<deckID>/<cardID>', methods=['GET', 'POST'])
def card_add(deckID, cardID):

    user.decks.add(deckID, cardID)
    return redirect(url_for('decks.edit', deckID=deckID))


@decks.route('/decks/<deckID>/<cardID>', methods=['GET', 'POST'])
def card_edit(deckID, cardID):

    if request.method == 'POST':
        if request.form.get('del-card') == 'del-card':
            user.decks.delete(deckID, cardID)
            return redirect(url_for('decks.edit', deckID=deckID))

    return render_template('card_edit.html', user=user, deckID=deckID, cardID=cardID, cardInfo=cardInfo, edit='deck')