import psycopg2
from psycopg2 import Error
from psycopg2 import *
from user_items import *

DB_USER = "postgres"
DB_PASS = "asdf" #"Conej0"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "postgres" #"Assign"

class User:
    def __init__(user, **kwargs): 
        conn = connect( 
            user=DB_USER,
            password=DB_PASS, 
            host=DB_HOST, 
            port=DB_PORT, 
            database=DB_NAME) # one DB for all users

        keys = kwargs.keys()
        if all(k in keys for k in ['username', 'password']):
            username = kwargs['username']
            password = kwargs['password']
            user.cursor = conn.cursor()
            user.cursor.execute('''
                SELECT userID
                FROM users
                WHERE username = %s AND password = %s;''',
                (username, password)
            )
            user.id = user.cursor.fetchone()[0]
            user.collection = Collection(user.id, conn)
            user.decks = Deck(user.id, conn)
        
        # cards in decks, list (deckID) of lists (cardID)
        user.cid = [] 

    def logout(user):
        user.cursor.close()
        user.connection.close()
