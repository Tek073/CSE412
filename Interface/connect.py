import psycopg2
from psycopg2 import Error
from psycopg2 import *
from user_items import *

DB_USER = "postgres"
DB_PASS = "asdf"

DB_HOST = "localhost"
DB_PORT = "5432"

class DBConnection:
    def __init__(user, username, password): 
        conn = connect( 
            user=DB_USER,
            password=DB_PASS, 
            host=DB_HOST, 
            port=DB_PORT, 
            database='postgres') # one DB for all users

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
        

    def logout(user):
        user.cursor.close()
        user.connection.close()
