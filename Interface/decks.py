from pokemontcgsdk import Card
from pokemontcgsdk import Set
from pokemontcgsdk import Type
from pokemontcgsdk import Supertype
from pokemontcgsdk import Subtype
from pokemontcgsdk import Rarity

from pokemontcgsdk import RestClient
RestClient.configure('') # API key goes here

class Collection:
    def __init__(user, someUser):
        user = someUser

    def get(user):
        user.cursor.execute(f"SELECT * FROM collection")

class Deck:

    def __init__(user, someUser):
        user = someUser
        deckID = 0

    def change(user, deckNum):
        user.deckID = deckNum

    def getCards(user):
        user.cursor.execute(f"SELECT * FROM decks WHERE deckID = {user.deckNum}")

    def size(user):
        user.cursor.execute(f"SELECT COUNT(*) FROM decks WHERE deckID = {user.deckNum}")




