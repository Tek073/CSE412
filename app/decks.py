from flask import Blueprint, redirect, render_template, request, url_for

from start import user
from globals import search_cards

cur = user.cursor
deck = user.decks
cardInfo = []

decks = Blueprint('decks', __name__)

@decks.route('/decks')
def list():

    decks = user.decks.getInfoFromAllDecks()
    return render_template('decks.html', user=user, decks=decks)

# Edit one specific deck. 
# NOTE: updates deckID
@decks.route('/decks/<deckID>', methods=['GET', 'POST'])
def edit(deckID):

    user.decks.changeTo(deckID)
    # Deck Search 
    if request.method == 'POST':
        data = dict(request.form)
        print(data)
        # # Legalities uses checkboxes. It's slightly more complicated.
        # # if both checkboxes checked, we don't care about legality. so remove them
        # legs = [['unlLeg','unlIll'],['expLeg','expIll'],['stdLeg','stdIll']]
        # for leg, ill in legs:
        #     if data.get(leg) != None and data.get(ill) != None: # both legal and illegal, i.e. doesn't matter
        #         del data[leg]
        #         del data[ill]
        #     elif data.get(ill) != None: # just illegal
        #         data[leg] = None # set leg to illegal
        #         del data[ill]
        #     # else just legal; no change required
        #     # else not legal nor illegal; impossible to determine,
        #     #    so instead ignore it, which is already done since both Nonetype

        # legs = ['unlLeg','expLeg','stdLeg']
        # for leg in legs:
        #     if data.get(leg) != None:
        #         if data[leg] == 'Illegal':
        #             data[leg] = None
        #         if data[leg] == 'Either':
        #             del data[leg]
 
        # w = ' AND '.join(cur.mogrify('%s = %%s' % key, [data[key]]).decode() for key in data)
        # print(w)
        
        if data.get('search-collection') != None:
            print('searching collection...')
            del data['search-collection']
            print(data)
            cardInfo = user.collection.search(data)
        if data.get('search-deck') != None:
            print('searching deck...')
            del data['search-deck']
            print(data)
            cardInfo = user.decks.search(data)

    else:
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

    if request.method == 'POST':
        if request.form.get('del-card') == 'del-card':
            user.decks.delete(deckID, cardID)
            return redirect(url_for('decks.edit', deckID=deckID))

    return render_template('card_edit.html', user=user, deckID=deckID, cardID=cardID, cardInfo=cardInfo)