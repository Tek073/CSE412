import sys
from psycopg2 import Error
from psycopg2 import *
import re

# in SQL, the Cards and Sets table is shared among all users
# Users will then have their own collection table, which draws from Cards
# And a deck table, which draws from their collection

from .api_calls import *
from globals import search_cards

class User:
    # Default guest login
    def __init__(user, conn):
        user.conn = conn
        user.cursor = conn.cursor()

        user.id = 0 # Guest ID
        user.username = 'Guest'
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
        user.username = username
        user.id = tempID
        user.collection = Collection(user)
        user.decks = Deck(user)

        return True

    # Logs out the user, by setting userID to guestID, 0
    def logout(user):
        user.id = 0
##############################################################
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
##############################################################
# Requires conn, and userID to only get data belonging to user
class Deck:
    def __init__(self, user):
        conn = user.conn
        self.userID = user.id
        self.conn = conn
        self.cursor = conn.cursor()
        self.deckIDList = []
        self.numDecks = 0
        self.deckID = 0
        self.deckName = 'default'

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
            self.deckName = 'placeholder'

    def create(self, deckName):
        if (self.numDecks >= 10):
            return False
        deckID = self.numDecks
        
        self.cursor.execute('''
            INSERT INTO decks
            VALUES (%s, %s, %s);
            ''',
            (self.userID, deckID, deckName)
        )
        
        self.numDecks += 1
        self.deckIDList.append(self.numDecks)

        return True

    # return list, where [n][0] is id, [n][1] is name for deckID = n
    def getInfoFromAllDecks(self):
        self.cursor.execute('''
        SELECT deckID, deckName 
        FROM decks 
        WHERE userID = %s''', 
        (self.userID,))
        return self.cursor.fetchall()

    # return list, where [0] is id, [1] is name
    def getInfoFromOneDeck(self, deckID):
        self.cursor.execute('''
        SELECT deckID, deckName 
        FROM decks 
        WHERE userID = %s 
        AND deckID = %s''', 
        (self.userID, deckID))
        return self.cursor.fetchone()

    # switch to another deck, by setting deckID and deckName
    def changeTo(self, deckID):
        self.deckID = deckID
        if (self.deckID == deckID):
            return
        deckInfo = self.getInfoFromOneDeck(deckID)
        self.deckName = deckInfo[1]

    # returns size, i.e. # of cards in a deck
    def size(self):
        self.cursor.execute('''
        SELECT COUNT(*) 
        FROM decks 
        WHERE userID = %s
        AND deckID = %s''',
        (self.userID, self.deckID)
        )

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
        except KeyError: # card already exists in deck; increment count instead

            # First check if count can be incremented
            self.cursor.execute('''
                SELECT count
                FROM _cards_in_decks
                WHERE userID = %s AND deckID = %s AND cardID = %s;''',
                (self.userID, deckID, cardID))
            if (self.cursor.fetchone()[0] >= 4):
                return False
            
            # Increment count
            self.cursor.execute('''
                UPDATE _cards_in_decks
                SET count = count + 1
                WHERE userID = %s AND deckID = %s AND cardID = %s AND count < 4;''',
                (self.userID, deckID, cardID))

            return True
            
        except (Exception, Error) as error:
            print(error)   

    # given deckID and cardID, removes 1 of that card from the deck
    def delete(self, deckID, cardID):

        # delete card if it's last of it's kind in deck
        self.cursor.execute('''
            DELETE FROM _cards_in_decks
            WHERE userID = %s AND deckID = %s AND cardID = %s AND count = 1;''',
            (self.userID, deckID, cardID))

        # else, decrement card's count
        if self.cursor.rowcount == 0:
            self.cursor.execute('''
                UPDATE _cards_in_decks
                SET count = count - 1
                WHERE userID = %s AND deckID = %s AND cardID = %s;''',
                (self.userID, deckID, cardID))
            if (self.cursor.rowcount == 0):
                return False

        return True




