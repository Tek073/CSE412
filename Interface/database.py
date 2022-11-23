import sys

from flask import Flask
from markupsafe import escape

import psycopg2
from psycopg2 import Error

from pokemontcgsdk import Card
from pokemontcgsdk import Set
from pokemontcgsdk import Type
from pokemontcgsdk import Supertype
from pokemontcgsdk import Subtype
from pokemontcgsdk import Rarity
from pokemontcgsdk import RestClient
RestClient.configure('92e6be5e-7d21-4d3e-9900-1753c97c0979') # Your API key goes here

from connect import *

DB_USER = "postgres"
DB_PASS = "asdf"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "ptcg_db"

# This was a test to get card info

#original_stdout = sys.stdout # Save a reference to the original standard output
# with open('pkmn_w_ability.txt', 'w') as f:
#     sys.stdout = f # Change the standard output to the file we created.
#     card = Card.find('bw1-6')1
#     #getNewSet('xy1')
#     print(card)
#     sys.stdout = original_stdout # Reset the standard output to its original value
#     exit

# ancient traits use special chars like α, which require utf-8 (as opposed to default ascii)
# with open('pkmn_w_ancientTrait.txt', 'w', encoding='utf-8') as f:
#     sys.stdout = f # Change the standard output to the file we created.
#     card = Card.find('xy5-104')
#     #getNewSet('xy1')
#     print(card)
#     sys.stdout = original_stdout # Reset the standard output to its original value
#     exit

user = DBConnection('asdf', 'asdf') # user in 'users' table; NOT the Database user, which will be the same for everyone

str = 'asdf, adsf, asdf'
asdf = user.cursor.mogrify('''
    INSERT INTO sets
    VALUES (%s);''',
    (str,) # psycopg2 tries to index into input, i.e. iterate over it. So we turn it into a tuple to allow this.
)
user_id = user.id
print(user.id)

# try:

#     #input("New user, or returning user?")

#     username = input("Username: ")
#     password = input("Passsword: ")

#     user = DBConnection(username, password)

#     option = input("""Type in # of option you want, or q to quit
#                         1: Add card to collection (ac)
#                         2: Add card to deck (ad)
#                         q: quit (q)\n""")

#     if option == 1:
#         # todo: search by other attributes
#         cardID = input('cardID: ')
#         user.addToCollection(cardID)
#         #print("ac")
#     elif option == 2:
#         # todo: search by other attributes
#         deckID = input('deckID: ')
#         cardID = input('cardID: ')
#         user.addToDeck(deckID, cardID)
#         #print("ad")
#     elif option == 'q':
#         print("quit")

# except (Exception, Error) as error:
#     print("Error while connecting to PostgreSQL: ", error)

# finally:
#     if (user.connection):
#         user.logout()
#         print("PostgreSQL connection is closed")

app = Flask(__name__)

@app.route("/")
def main():
    return "<p>Pokemon Trading Card Gallery!!!!!!!!!!!!!!!!!!!!!!</p>"

@app.route("/<user_id>/decks")
def decks(user_id = user.id, deck_id = user.decks):
    return "<p>decks</p>"