-- Online SQL Editor to Run SQL Online.
-- Use the editor to create new tables, insert data and all other SQL operations.
  
CREATE TABLE card (
  id int,
  nameCard varchar(55),
  rarity int,   -- out of 10
  artist varchar(55),
  regulationMark int,
  PRIMARY KEY (id)
  -- add more foreign keys later
);

-- list of some artists for reference
/*
Yuka Morii, Ken Sugimori, Kagemaru Himeno,
Tokiya, Atsuko Nishida, Fumi Kusube
(will make up names for sake of inserts also)
*/

INSERT INTO card
VALUES
  (1, 'biddof', 4, 'Yuka Morii', 1),
  (

  
