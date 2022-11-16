CREATE TABLE users (
  userID int,
  username varchar(255),
  'password' varchar(255), 

  PRIMARY KEY (userID)
);

-- SELECT cards.* 
-- FROM users, _collection, cards  
-- WHERE users.userID = _collection.userID AND _collection.cardID = cards.cardID