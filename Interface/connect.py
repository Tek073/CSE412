import psycopg2
from psycopg2 import Error
from psycopg2 import *
from user_items import *
from flask import flash


DB_USER = "postgres"
DB_PASS = "asdf" #"Conej0"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "postgres" #"Assign"

class DBConnection:
    def __init__(user, **kwargs): 
        conn = connect( 
            user=DB_USER,
            password=DB_PASS, 
            host=DB_HOST, 
            port=DB_PORT, 
            database=DB_NAME) # one DB for all users

        user.cursor = conn.cursor()
        print(user.cursor.connection)
        user.cursor.execute("SELECT version();")
        record = user.cursor.fetchone()
        print("You are connected to - ", record, "\n")

        keys = kwargs.keys()
        if all(k in keys for k in ['username', 'password']):
            username = kwargs['username']
            password = kwargs['password']
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

class addUser:
    def __init__(user, username, password) -> None:
        
        conn = connect( 
            user=DB_USER,
            password=DB_PASS, 
            host=DB_HOST, 
            port=DB_PORT, 
            database='Assign') # one DB for all users

        user.cursor = conn.cursor()
        print(user.cursor.connection)
        user.cursor.execute('''
        SELECT COUNT(*) FROM users;'''
        )
        print("COUNT")
        results = user.cursor.fetchone()[0]
        id = results + 1
        user.cursor.execute('''
            INSERT INTO users
                VALUES (%s, %s, %s);''',
                (id, username, password)
        )
        print(user.cursor.execute('''
            SELECT FROM users;'''))
        conn.commit()
        conn.close()

class loginUser:
    def __init__(user, username, password) -> None:
        
        conn = connect( 
            user=DB_USER,
            password=DB_PASS, 
            host=DB_HOST, 
            port=DB_PORT, 
            database='Assign') # one DB for all users

        user.cursor = conn.cursor()
        print(user.cursor.connection)
        
        print(user.cursor.execute('''
            SELECT FROM users;'''))
