import sys
import psycopg2
from psycopg2 import Error

from pokemontcgsdk import Card
from pokemontcgsdk import Set
from pokemontcgsdk import Type
from pokemontcgsdk import Supertype
from pokemontcgsdk import Subtype
from pokemontcgsdk import Rarity

from pokemontcgsdk import RestClient
RestClient.configure('') # Your API key goes here

DB_USER = "postgres"
DB_PASS = "asdf"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "ptcg_db"

from connect import *
from decks import *

try:
    # This was a test to get card info
    original_stdout = sys.stdout # Save a reference to the original standard output
    with open('filename.txt', 'w') as f:
        sys.stdout = f # Change the standard output to the file we created.
        card = Card.find('xy1-1')
        print(card)
        sys.stdout = original_stdout # Reset the standard output to its original value
        exit

    #input("New user, or returning user?")
    username = input("Username: ")
    password = input("Passsword: ")

    user = Connection(username, password)

    option = input("""Type in # of option you want, or q to quit
                        1: Add card to collection (ac)
                        2: Add card to deck (ad)
                        q: quit (q)\n""")

    if option == 1:
        print("ac")
    elif option == 2:
        print("ad")
    elif option == 'q':
        print("quit")

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL: ", error)

finally:
    if (user.connection):
        user.logout()
        print("PostgreSQL connection is closed")