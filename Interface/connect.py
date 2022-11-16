import psycopg2
from psycopg2 import Error
from decks import *

DB_HOST = "localhost"
DB_PORT = "5432"

class Connection:
    def __init__(user, DB_USER, DB_PASS): # this is basically user login
        user.connection = psycopg2.connect( user=DB_USER,
                                            password=DB_PASS, 
                                            host=DB_HOST, 
                                            port=DB_PORT, 
                                            database='PTCG_DB') # we are NOT going to use separate DB for users.
                                                            # searching online, apparently it's kind of a bad idea
        user.cursor = user.connection.cursor()
        user.deck = Deck(user)

    def logout(user):
        user.cursor.close()
        user.connection.close()
