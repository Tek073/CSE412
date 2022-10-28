-- create Legalitites table
CREATE TABLE Legalitites (
  nameOfLegalCompetition varchar(100) NOT NULL,
  text varchar(100),
  PRIMARY KEY (nameOfLegalCompetition)
);

-- fill Legalitites table
INSERT INTO Legalitites
VALUES
  ('standard', 'The card is legal only in standard competitions'),
  ('expanded', 'The card is legal only in expanded competitions'),
  ('unlimited', 'The card is legal only in unlimted competitions'),
  ('all competitions', 'The card is legal in all competitions'),
  ('unlimited and standard', 'The card is legal only in unlimited and standard competitions'),
  ('expanded and standard', 'The card is legal only in expanded and standard competitions'),
  ('expanded and unlimited', 'The card is legal only in expanded and unlimited competitions');
  
-- show Legalitites table
SELECT * FROM Legalitites;
