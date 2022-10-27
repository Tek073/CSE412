
-- create resistance table
CREATE TABLE resistances (
  type varchar(55),
  value int,
  PRIMARY KEY (type, value)
);

-- insert values into table
INSERT INTO resistances
VALUES
  ('water', 2),
  ('fire', 2),
  ('grass', 2),
  ('fighting', 2),
  ('rock', 1),
  ('ground', 1),
  ('dark', 1),
  ('flying', 1),
  ('ice', 1),
  ('bug', 2);
  
-- show resistances table is filled
SELECT * FROM resistances
