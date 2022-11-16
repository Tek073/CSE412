-- create weaknesses table
CREATE TABLE weaknesses (
  id varchar(20),
  typeWeaknesses varchar(55),
  valueWeaknesses varchar(5), -- e.g. 1.5
  PRIMARY KEY (typeWeaknesses, valueWeaknesses)
  FOREIGN KEY (id) REFERENCES pokemon(id)
);

-- weaknesses simultaneously with card info
-- -- insert into weaknesses
-- INSERT INTO weaknesses
-- VALUES
--   ('water', 2),
--   ('fire', 2),
--   ('grass', 2),
--   ('bug', 2),
--   ('rock', 2),
--   ('water', 1),
--   ('fire', 1),
--   ('grass', 1),
--   ('dark', 1),
--   ('fairy', 1),
--   ('steel', 1),
--   ('dragon', 1);
  
-- -- show weaknesses are filled
-- SELECT * FROM weaknesses 
