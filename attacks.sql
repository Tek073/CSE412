-- create table attacks
CREATE TABLE attacks (
  id VARCHAR(20),
  nameAttack varchar(55) NOT NULL,
  cost int,
  damage int,
  text varchar(55),
  PRIMARY KEY (id, nameAttack),
  FOREIGN KEY (id) REFERENCES (pokemon)
);

-- attacks added simultaneously with card info
-- -- fill table attacks
-- INSERT INTO attacks 
-- VALUES 
--   ('tackle', 2, 'charge the opponent', 20),
--   ('pound', 2, 'pound the pokemon', 30),
--   ('scratch', 1, 'scratch the pokemon', 25),
--   ('bite', 3, 'bite the pokemon', 60),
--   ('blizzard', 5, 'create a blizzrd', 110),
--   ('ember', 2, 'burn enemy', 40),
--   ('cut', 1, 'cut pokemon', 20),
--   ('double kick', 4, 'double kick pokemon', 75);

-- -- show that attacks table is full
-- -- SELECT * FROM attacks;
