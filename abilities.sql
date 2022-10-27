-- create abilities table
CREATE TABLE abilities (
  name varchar(55) NOT NULL,
  text varchar(55),
  type varchar(55),
  PRIMARY KEY (name)
);

-- fill abilities table
INSERT INTO abilities
VALUES
  ('harden', 'increase pokemons defense', 'normal'),
  ('charm', 'lower enemy attack', 'fairy'),
  ('leer', 'lower enemy defense', 'normal'),
  ('double team', 'increase evade stat', 'normal'),
  ('sharpen', 'increase special attack', 'normal'),
  ('confusion', 'inflict confusion', 'psychic'),
  ('hail', 'increase ice attacks', 'ice'),
  ('sunny day', 'increase fire attacks', 'fire'),
  ('water sprout', 'increase water attacks', 'water'),
  ('toxic thread', 'poison enemy', 'poison');
  
-- show abilities table
-- SELECT * FROM abilities;
