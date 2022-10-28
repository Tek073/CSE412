--- this is the collection of cards
CREATE TABLE cards (
  cardID VARCHAR(20),
  userID int,
  count int, -- duplicate cards increment count

  name VARCHAR(55),
  supertype VARCHAR(20), -- e.g. pokemon, energy, trainer
  subtypes VARCHAR(30) ARRAY[10], -- Basic, EX, Mega, Rapid Strike etc.
  types VARCHAR(30) ARRAY[10],
  rules VARCHAR(255) ARRAY[10],

  setID VARCHAR(20), -- if setID does not exist in sets, add it to sets.

  number VARCHAR(4), -- # in set. Assuming set size < 1000
  artist VARCHAR(50),
  rarity VARCHAR(30), -- e.g. "Common", "Rare Rainbow"
  flavorText VARCHAR(500),

  unlLeg VARCHAR(10),
  expLeg VARCHAR(10),
  stdLeg VARCHAR(10),
  --legalities CHAR(10) ARRAY[VARCHAR(20)];

  regMark CHAR(1), -- Letter symbol
  smallImage VARCHAR(255), -- URL
  largeImage VARCHAR(255), -- URL; could be quite long
  
  PRIMARY KEY (cardID),
  FOREIGN KEY (userID) REFERENCES (user),
  FOREIGN KEY (setID) REFERENCES (sets) -- set added first, then the card. cards has FK, b/c it is 'many' in many-to-1 rel with sets
);

CREATE TABLE pokemon (
  id VARCHAR(20),
  level int,
  hp int,
  pxdx int,
  evolvesTo varchar(55),
  evolvesFrom varchar(55),
  -- typeWeaknesses varchar(55),
  -- valueWeaknesses varchar(5), -- e.g. 1.5
  -- typeResistances varchar(55),
  -- valueResistances varchar(5), -- e.g. 0.5
  PRIMARY KEY (id),
  FOREIGN KEY (id) REFERENCES cards(id), -- inherits card info
);

-- create table attacks
CREATE TABLE attacks (
  id VARCHAR(20),
  nameAttack varchar(55) NOT NULL,
  cost int,
  text varchar(55),
  damage int,
  PRIMARY KEY (id, nameAttack),
  FOREIGN KEY (id) REFERENCES (pokemon)
);

-- There is a hiearachy to inserts; sets -> cards -> pokemon -> attacks, abilities, types
INSERT INTO 'sets' VALUES
('swsh9', "Sword & Shield Brilliant Stars", "Sword & Shield Brilliant Stars", 172, 999, "Legal", "Banned", NULL, "Blah", "Blah", "Blah", 
  "https://images.pokemontcg.io/swsh9/symbol.png", "https://images.pokemontcg.io/swsh9/logo.png");
INSERT INTO cards VALUES 
('swsh9-87', 1, 1, 'Weavile', 'Pokemon', '{"Basic"}', '{"Darkness"}', '{"Rules go here"}', 
  'swsh9', 150, "Hasuno", "Common", "Flavor Text", "Legal", "Banned", NULL,
  'F', "https://images.pokemontcg.io/swsh9/87.png", "https://images.pokemontcg.io/swsh9/87_hires.png");
INSERT INTO pokemon VALUES
('swsh9-87', 10, 100, 461, "Sneasel", NULL);
INSERT INTO attacks VALUES
('swsh9-87', 'Ransack', 1, 0, 'Flip 2 coins. If either of them is heads, your opponent reveals their hand. 
  For each heads, choose a card you find there and put it on the bottom of your opponent’s deck in any order.'),
('swsh9-87', 'Slash', 3, 100, NULL);
INSERT INTO weaknesses VALUES 
('swsh9-87', 'Grass', '2');
-- no resistances
-- no abilities

INSERT INTO 'sets' VALUES
('xy1', "XY", "XY", 146, 146, "Legal", "Legal", NULL, 'XY', '2014/02/05', '2018/03/04 10:35:00', 
  'https://images.pokemontcg.io/xy1/symbol.png', 'https://images.pokemontcg.io/xy1/logo.png');
INSERT INTO cards VALUES 
('xy1-1', 1, 1, 'Venusaur-EX', 'Pokemon', '{"Basic", "EX"}', '{"Grass"}', '{"Pokémon-EX rule: When a Pokémon-EX has been Knocked Out, your opponent takes 2 Prize cards."}', 
  'xy1', 1, 'Eske Yoshinob', 'Rare Holo EX', NULL, "Legal", "Legal", NULL,
  NULL, "https://images.pokemontcg.io/xy1/1.png", "https://images.pokemontcg.io/xy1/1_hires.png");
INSERT INTO pokemon VALUES
('xy1-1', 10, 180, 461, NULL, NULL);
INSERT INTO attacks VALUES
('xy1-1', 'Poison Powder', 3, 60, "Your opponent's Active Pokémon is now Poisoned."),
('xy1-1', 'Jungle Hammer', 4, 90, 'Heal 30 damage from this Pokémon.');
INSERT INTO weaknesses VALUES 
('xy1-1', 'Fire', '2');
-- no resistances
-- no abilities
