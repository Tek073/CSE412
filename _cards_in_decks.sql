-- decks have 1-60 cards, and up to 4 duplicates
CREATE TABLE _cards_in_decks (
  deckID int,
  cardID varchar(20),
  count int, -- Using count variable allows duplicates, since it doesn't make the primary key refer to more than 1 row
             -- Count variable preferable to, e.g. deckSlot, since mixing insert/delete doesn't mess it up
 
  PRIMARY KEY (deckID, cardID),
  FOREIGN KEY (deckID) REFERENCES (decks), -- makes sure deck exists
  FOREIGN KEY (cardID) REFERENCES (cards) -- checks card exists in collection
);

-- insert to add cards to a deck
