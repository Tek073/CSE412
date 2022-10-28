-- create legalities Table
CREATE TABLE Legalities (
  nameOfLegalCompetition varchar(100) NOT NULL,
  text varchar(100),
  PRIMARY KEY (nameOfLegalCompetition)
);

-- fill abilities table
INSERT INTO Legalities
VALUES
  ('standard', 'The card is legal only in standard competitions'),
  ('expanded', 'The card is legal only in expanded competitions'),
  ('unlimited', 'The card is legal only in unlimted competitions'),
  ('all competitions', 'The card is legal in all competitions'),
  ('unlimited and standard', 'The card is legal only in unlimited and standard competitions'),
  ('expanded and standard', 'The card is legal only in expanded and standard competitions'),
  ('expanded and unlimited', 'The card is legal only in expanded and unlimited competitions');

-- create abilities table
CREATE TABLE abilities (
  nameAbility varchar(55) NOT NULL,
  text varchar(555),
  type varchar(55),
  PRIMARY KEY (nameAbility)
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
  ('n/a', 'the pokemon has no ability', 'n/a'),
  ('toxic thread', 'poison enemy', 'poison');
  
-- create table attacks
CREATE TABLE attacks (
  nameAttack varchar(55) NOT NULL,
  cost int,
  text varchar(55),
  damage int,
  PRIMARY KEY (nameAttack)
);

-- fill table attacks
INSERT INTO attacks 
VALUES 
  ('tackle', 2, 'charge the opponent', 20),
  ('pound', 2, 'pound the pokemon', 30),
  ('scratch', 1, 'scratch the pokemon', 25),
  ('bite', 3, 'bite the pokemon', 60),
  ('blizzard', 5, 'create a blizzrd', 110),
  ('ember', 2, 'burn enemy', 40),
  ('cut', 1, 'cut pokemon', 20),
  ('Dancing Shuriken', 3, 'Throw 3 shurikens', 210),
  ('double kick', 4, 'double kick pokemon', 75);
  
-- create resistance table
CREATE TABLE resistances (
  typeResistances varchar(55),
  valueResistances int,
  PRIMARY KEY (typeResistances, valueResistances)
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

-- create weaknesses table
CREATE TABLE weaknesses (
  typeWeaknesses varchar(55),
  valueWeaknesses int,
  PRIMARY KEY (typeWeaknesses, valueWeaknesses)
);

-- insert into weaknesses
INSERT INTO weaknesses
VALUES
  ('water', 2),
  ('fire', 2),
  ('grass', 2),
  ('bug', 2),
  ('rock', 2),
  ('water', 1),
  ('fire', 1),
  ('grass', 1),
  ('dark', 1),
  ('fairy', 1),
  ('steel', 1),
  ('Lightning', 2),
  ('dragon', 1);
  

CREATE TABLE pokemon (
  namePokemon varchar(55),
  level int,
  hp int,
  pxdx int,
  evolvesTo varchar(55),
  evolvesFrom varchar(55),
  nameAbility varchar(55),
  nameAttack varchar(55),
  typeWeaknesses varchar(55),
  valueWeaknesses int,
  typeResistances varchar(55),
  valueResistances int,
  legalities varchar(100),
  PRIMARY KEY (pxdx),
  FOREIGN KEY (legalities) REFERENCES Legalities(nameOfLegalCompetition),
  FOREIGN KEY (nameAbility) REFERENCES abilities(nameAbility),
  FOREIGN KEY (nameAttack) REFERENCES attacks(nameAttack),
  FOREIGN KEY (typeWeaknesses, valueWeaknesses) REFERENCES weaknesses(typeWeaknesses, valueWeaknesses),
  FOREIGN KEY (typeResistances, valueResistances) REFERENCES resistances(typeResistances, valueResistances)
);

INSERT INTO pokemon
VALUES
  ('biddof', 12, 33, 1, 'barbarrel', 'n/a', 'harden', 'pound', 'fire', 2, 'water', 2, 'standard'),
  ('Greninja V', NULL , 210, 658, 'n/a', 'n/a', 'n/a', 'Dancing Shuriken', 'Lightning', 2, 'n/a', NULL, 'expanded');
  
SELECT * FROM pokemon
