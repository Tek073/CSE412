/*
THIS CODE IS DEPENDENT ON A TABLE NAMED 'card' BEING INSTANTIATED
also card must have a variable 'id' with type 'int' in it
*/

-- create energy table
CREATE TABLE energy (
  type varchar(55),
  value int,
  -- id is dependent on card table existing
  id int NOT NULL REFERENCES cards(id),
  PRIMARY KEY(id)
);

-- assuming that id of energy cards are 50 - 59
INSERT INTO energy
VALUES
  ('fire', 1, 50),
  ('water', 1, 51),
  ('fire', 1, 52),
  ('ice', 1, 53),
  ('dark', 1, 54),
  ('rock', 1, 55),
  ('lightning', 1, 56),
  ('dragon', 1, 57),
  ('grass', 1, 58),
  ('ground', 1, 59);
