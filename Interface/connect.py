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
    # Establishes DB connection
    def __init__(DB): 
        DB.conn = connect( 
            user=DB_USER,
            password=DB_PASS, 
            host=DB_HOST, 
            port=DB_PORT, 
            database=DB_NAME) # one DB for all users
        DB.cursor = DB.conn.cursor()
        DB.cursor.execute("SELECT version();")
        record = DB.cursor.fetchone()
        print("You are connected to - ", record, "\n")

    # Close the DB connection
    def close(DB):
        DB.cursor.close()
        DB.conn.close()

class User:
    # Default guest login
    def __init__(user, conn):
        user.conn = conn
        user.cursor = conn.cursor()
        user.id = 0 # Guest ID
        user.cid = []  # cards in decks, list (deckID) of lists (cardID)
        user.decks = Deck(user)
        user.collection = Collection(user)

    # Takes username and password. Attempts to register new user with it; true if success, false otherwise
    def signup(user, username, password):
        conn = user.conn
        user.cursor = conn.cursor()
        #print(user.cursor.connection)

        user.cursor.execute('''
            SELECT username
            FROM users
            WHERE username = %s;''',
            (username,)
        )
        if (user.cursor.fetchone() != None):
            return False

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

        #user.id = id Not logging in yet; save it for login
        return True

    # Takes in username and password and attempts login. Returns true if success, otherwise false
    def login(user, username, password):
        # keys = kwargs.keys()
        # if all(k in keys for k in ['username', 'password']):
        #     username = kwargs['username']
        #     password = kwargs['password']
        user.cursor.execute('''
            SELECT userID
            FROM users
            WHERE username = %s AND password = %s;''',
            (username, password)
        )

        tempID = user.cursor.fetchone()
        if (tempID == None):
            return False
        user.id = tempID
        user.collection = Collection(user)
        user.decks = Deck(user)

        return True

    # Logs out the user, by setting userID to guestID, 0
    def logout(user):
        user.id = 0

# class addUser:
#     def __init__(user, username, password) -> None:
        
#         conn = connect( 
#             user=DB_USER,
#             password=DB_PASS, 
#             host=DB_HOST, 
#             port=DB_PORT, 
#             database=DB_NAME)

#         user.cursor = conn.cursor()
#         print(user.cursor.connection)
#         user.cursor.execute('''
#         SELECT COUNT(*) FROM users;'''
#         )
#         print("COUNT")
#         results = user.cursor.fetchone()[0]
#         id = results + 1
#         user.cursor.execute('''
#             INSERT INTO users
#                 VALUES (%s, %s, %s);''',
#                 (id, username, password)
#         )
#         print(user.cursor.execute('''
#             SELECT FROM users;'''))
#         conn.commit()
#         conn.close()

# class loginUser:
#     def __init__(user, username, password) -> None:
        
#         conn = connect( 
#             user=DB_USER,
#             password=DB_PASS, 
#             host=DB_HOST, 
#             port=DB_PORT, 
#             database='Assign') # one DB for all users

#         user.cursor = conn.cursor()
#         print(user.cursor.connection)
        
#         print(user.cursor.execute('''
#             SELECT FROM users;'''))
