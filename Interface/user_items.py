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

# in SQL, the Cards and Sets table is shared among all users
# Users will then have their own collection table, which draws from Cards
# And a deck table, which draws from their collection

from api_calls import *
from global_items import *

# returns list of cardIDs that match with search parameter

class Collection:
    def __init__(self, id, conn):
        self.conn = conn
        self.id = id
        self.cursor = conn.cursor()
    
    # return cardIDs and counts of cards in collection, given search parameters
    def search(self, **kwargs):
        found = []
        cardIDs = search_cards(self.cursor, **kwargs)
        for cardID in cardIDs:
            self.cursor.execute('''
                SELECT cardID, count
                FROM _cards_in_collections
                WHERE userID = %s AND cardID = %s''',
                (self.id, cardID))
            found.append(self.cursor.fetchone())
        return found

    # add card by cardID into Collection
    def add(self, cardID):
        #keys = kwargs.keys
        try:
            #addIfNewCard(self, **kwargs)
            # self.cursor.execute('''SELECT cardID FROM cards WHERE cardID = %s''', keys["cardID"])
            # self.cursor.execute('''SELECT cardID FROM cards WHERE cardID = %s''', keys["name"])

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
        self.numDecks = len(self.deckIDList) # deckID from 1-10
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
    def getAllDeckInfo(self):
        self.cursor.execute('''SELECT deckID, deckname FROM decks WHERE userID = %s''', self.id)
        return self.cursor.fetchall()

    def changeTo(self, deckID):
        self.deckID = deckID

    def getCards(self):
        self.cursor.execute(f"SELECT * FROM decks WHERE deckID = {self.deckNum}")

    def size(self):
        self.cursor.execute(f"SELECT COUNT(*) FROM decks WHERE deckID = {self.deckNum}")

    # returns cardIDs and counts for cards in deck, given parameters
    def search(self, **kwargs):
        found = []
        cardIDs = search_cards(self.cursor, **kwargs)
        for cardID in cardIDs:
            self.cursor.execute('''
                SELECT cardID, count
                FROM decks
                WHERE userID = %s AND deckID = %s AND cardID = %s''',
                (self.id, self.deckID, cardID))
            found.append(self.cursor.fetchone())
        return found

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




