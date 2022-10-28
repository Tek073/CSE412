-- create resistance table
CREATE TABLE resistances (
  id varchar(20),
  typeResistances varchar(55),
  valueResistances varchar(5), -- e.g. 0.5
  PRIMARY KEY (typeResistances, valueResistances)
  FOREIGN KEY (id) REFERENCES pokemon(id)
);

-- resistances added simultaneously with card info
-- -- insert values into table
-- INSERT INTO resistances
-- VALUES
--   ('water', 2),
--   ('fire', 2),
--   ('grass', 2),
--   ('fighting', 2),
--   ('rock', 1),
--   ('ground', 1),
--   ('dark', 1),
--   ('flying', 1),
--   ('ice', 1),
--   ('bug', 2);
  
-- -- show resistances table is filled
-- SELECT * FROM resistances
