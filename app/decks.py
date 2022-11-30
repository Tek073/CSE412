from flask import Blueprint, redirect, render_template, request, url_for


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

    cur.execute('''
        SELECT cards.cardID, cards.name, count, largeImage
        FROM _cards_in_decks, cards
        WHERE userID = %s
        AND deckID = %s
        AND _cards_in_decks.cardID = cards.cardID''',
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
        if request.form['del-card'] == 'del-card':
            user.decks.delete(deckID, cardID)
            return redirect(url_for('decks.edit', deckID=deckID))

    return render_template('card_edit.html', deckID=deckID, cardID=cardID, cardInfo=cardInfo)
    return f'<h1>DeckID: {deckID}. This card is #{numInDeck} in deck'