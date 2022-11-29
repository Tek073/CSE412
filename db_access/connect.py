import psycopg2
from psycopg2 import Error
from psycopg2 import *
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
