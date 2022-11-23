import sys
import psycopg2
from psycopg2 import Error
from psycopg2 import *

from pokemontcgsdk import Card
from pokemontcgsdk import Set
from pokemontcgsdk import Type
from pokemontcgsdk import Supertype
from pokemontcgsdk import Subtype
from pokemontcgsdk import Rarity

import re
from pokemontcgsdk import RestClient
#RestClient.configure('92e6be5e-7d21-4d3e-9900-1753c97c0979') # API key goes here

# in SQL, the Cards and Sets table is shared among all users
# Users will then have their own collection table, which draws from Cards
# And a deck table, which draws from their collection

from api_calls import *

class Collection:
    def __init__(self, id, conn):
        self.conn = conn
        self.id = id
        self.cursor = conn.cursor()

    def add(self, cardID):
        try:
            addIfNewCard(self, cardID)
            self.cursor.execute('''
                INSERT INTO _cards_in_collections
                VALUES (%s, %s, 1);''', 
                (self.id, cardID))
        except KeyError:
            self.cursor.execute('''
                UPDATE _cards_in_collections
                SET count = count + 1
                WHERE userID = %s AND cardID = %s;''', 
                (self.id, cardID))

    def subtract(self, cardID, count : int):
        self.cursor.execute('''
            SELECT count
            FROM _cards_in_collections
            WHERE userID = %s AND cardID = %s;''',
            (self.id, cardID))
        currCount = self.cursor.fetchone()[0]

        if (count > currCount):
            count = currCount

        self.cursor.execute('''
            UPDATE _cards_in_collections
            SET count = count - %s
            WHERE userID = %s AND cardID = %s;''', 
            (count, self.id, cardID))

    def delete(self, cardID):
        self.cursor.execute('''
            DELETE FROM _cards_in_collections
            WHERE userID = %s AND cardID = %s;''', 
            (self.id, cardID))

    def get(self):
        self.cursor.execute(f"SELECT * FROM collection")

class Deck:
    def __init__(self, id, conn):
        self.conn = conn
        self.id = id
        self.cursor = conn.cursor()

        self.cursor.execute('''
            SELECT deckID
            FROM decks
            WHERE userID = %s;''',
            (self.id,)) 
        
        self.deckIDList = self.cursor.fetchall() # array of ints
        self.numDecks = len(self.deckIDList)
        self.deckID = self.deckIDList[0] # arbitrarily make default deckID 1st one in list

    def create(self, deckName):
        if (self.numDecks >= 10):
            return
        deckID = self.numDecks
        self.numDecks += 1
        
        self.cursor.execute('''
            INSERT INTO decks
            VALUES (%s, %s, %s);
            ''',
            (self.id, deckID, deckName)
        )

    def changeTo(self, deckID):
        self.deckID = deckID

    def getCards(self):
        self.cursor.execute(f"SELECT * FROM decks WHERE deckID = {self.deckNum}")

    def size(self):
        self.cursor.execute(f"SELECT COUNT(*) FROM decks WHERE deckID = {self.deckNum}")

    def add(self, deckID, cardID):
        try:
            self.cursor.execute('''
                INSERT INTO _cards_in_decks
                VALUES (%s, %s, %s, 1);''',
                (self.id, deckID, cardID))
        except KeyError: #card already exists in deck; increment count instead
            self.cursor.execute('''
                SELECT count
                FROM _cards_in_decks
                WHERE deckID = %s AND cardID = %s;''',
                (deckID, cardID))
            if (self.cursor.fetchone()[0] >= 4):
                return False
            
            self.cursor.execute('''
                UPDATE _cards_in_decks
                SET count = count + 1
                WHERE deckID = %s AND cardID = %s AND count < 4;''',
                (deckID, cardID))

            return True
            
        except (Exception, Error) as error:
            print(error)   




