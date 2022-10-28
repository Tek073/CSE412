--- this is the collection of cards
CREATE TABLE cards (
  cardID VARCHAR(20),
  userID int,
  count int, -- duplicate cards increment count

  name VARCHAR(55),
  supertype VARCHAR(20),
  subtypes VARCHAR(30) ARRAY[10], 
  types VARCHAR(30) ARRAY[10],
  rules VARCHAR(255) ARRAY[10],

  setID VARCHAR(20),

  number VARCHAR(4), -- # in deck. Assuming deck size < 1000
  artist VARCHAR(50),
  rarity VARCHAR(30), -- e.g. "Common", "Rare Rainbow"
  flavorText VARCHAR(500),

  stdLeg VARCHAR(10),
  expLeg VARCHAR(10),
  unlLeg VARCHAR(10),

  regMark CHAR(1), -- Letter symbol
  smallImage VARCHAR(255), -- URL
  largeImage VARCHAR(255), -- URL; could be quite long
  
  PRIMARY KEY (cardID),
  FOREIGN KEY (userID) REFERENCES (user),
  FOREIGN KEY (setID) REFERENCES (sets) -- set added first, then the card
);

