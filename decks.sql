CREATE TABLE decks (
  deckID int,
  userID int,
  cardID varchar(20),
  deckName varchar(255),
  
  PRIMARY KEY (deckID),
  FOREIGN KEY (userID) REFERENCES (user)
  FOREIGN KEY (cardID) REFERENCES (_cards_in_decks)
);

-- insert to create new deck
