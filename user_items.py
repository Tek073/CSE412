import sys
from psycopg2 import Error
from psycopg2 import *
import re

# in SQL, the Cards and Sets table is shared among all users
# Users will then have their own collection table, which draws from Cards
# And a deck table, which draws from their collection

from interface.api_calls import *
from globals import search_cards

# returns list of cardIDs that match with search parameter

# Requires conn, and userID to only get data belonging to user
class Collection:
    def __init__(self, user):
        conn = user.conn
        self.conn = conn
        self.userID = user.id
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
                (self.userID, cardID))
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
                (self.userID, cardID))
        except KeyError:
            self.cursor.execute('''
                UPDATE _cards_in_collections
                SET count = count + 1
                WHERE userID = %s AND cardID = %s;''', 
                (self.userID, cardID))

    def subtract(self, cardID, count : int):
        self.cursor.execute('''
            SELECT count
            FROM _cards_in_collections
            WHERE userID = %s AND cardID = %s;''',
            (self.userID, cardID))
        currCount = self.cursor.fetchone()[0]

        if (count > currCount):
            count = currCount

        self.cursor.execute('''
            UPDATE _cards_in_collections
            SET count = count - %s
            WHERE userID = %s AND cardID = %s;''', 
            (count, self.userID, cardID))

    def delete(self, cardID):
        self.cursor.execute('''
            DELETE FROM _cards_in_collections
            WHERE userID = %s AND cardID = %s;''', 
            (self.userID, cardID))

    def get(self):
        self.cursor.execute(f"SELECT * FROM collection")

# Requires conn, and userID to only get data belonging to user
class Deck:
    def __init__(self, user):
        conn = user.conn
        self.userID = user.id
        self.conn = conn
        self.cursor = conn.cursor()

        self.cursor.execute('''
            SELECT deckID
            FROM decks
            WHERE userID = %s;''',
            (self.userID,)) 
        
        temp = self.cursor.fetchall()
        print(temp)
        # If at least 1 deck
        if (len(temp) > 0): # fetchall does not return None
            self.deckIDList = temp # list of ints
            self.numDecks = len(self.deckIDList) # deckID from 1-10
            self.deckID = self.deckIDList[0] # arbitrarily make default deckID 1st one in list
        # else if no decks
        else:
            self.deckIDList = []
            self.numDecks = 0
            self.deckID = 0

    def create(self, deckName):
        if (self.numDecks >= 10):
            return
        deckID = self.numDecks
        
        self.cursor.execute('''
            INSERT INTO decks
            VALUES (%s, %s, %s);
            ''',
            (self.userID, deckID, deckName)
        )
        self.numDecks += 1
        self.deckIDList.append(self.numDecks)

    def getAllDeckInfo(self):
        self.cursor.execute('''SELECT deckID, deckname FROM decks WHERE userID = %s''', self.userID)
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
                (self.userID, self.deckID, cardID))
            found.append(self.cursor.fetchone())
        return found

    def add(self, deckID, cardID):
        try:
            self.cursor.execute('''
                INSERT INTO _cards_in_decks
                VALUES (%s, %s, %s, 1);''',
                (self.userID, deckID, cardID))
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




