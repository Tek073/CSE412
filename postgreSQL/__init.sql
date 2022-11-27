-------------------------------
-- DECLARATION ----------------
-------------------------------

DROP TABLE IF EXISTS resistances;
DROP TABLE IF EXISTS weaknesses;
DROP TABLE IF EXISTS abilities;
DROP TABLE IF EXISTS attacks;
DROP TABLE IF EXISTS pokemon;
DROP TABLE IF EXISTS _cards_in_collections;
DROP TABLE IF EXISTS _cards_in_decks;
DROP TABLE IF EXISTS cards;
DROP TABLE IF EXISTS sets;
DROP TABLE IF EXISTS decks;
DROP TABLE IF EXISTS users;

-- create a user
DROP TABLE IF EXISTS users;
CREATE TABLE users (
  userID int,
  username varchar(255),
  password varchar(255), 

  PRIMARY KEY (userID)
);

-- create a user's deck
DROP TABLE IF EXISTS decks;
CREATE TABLE decks (
  userID int,
  deckID int,
  deckName varchar(255),
  
  PRIMARY KEY (deckID),
  FOREIGN KEY (userID) REFERENCES users
);

-- list of sets that cards from all users belong to
DROP TABLE IF EXISTS sets;
CREATE TABLE sets (
  setID VARCHAR(20), -- e.g. "swsh1"

  name VARCHAR(55),
  series VARCHAR(55),
  printedTotal INT,
  total INT,

  unlLeg VARCHAR(10),
  expLeg VARCHAR(10),
  stdLeg VARCHAR(10),

  ptcgoCode VARCHAR(55),
  releaseDate VARCHAR(55),
  updatedAt VARCHAR(55),

  symbol VARCHAR(255),
  logo VARCHAR(255),

  PRIMARY KEY (setID)
  --FOREIGN KEY (setID) REFERENCES cards(setID)
);

--- this is collection of cards across ALL users
DROP TABLE IF EXISTS cards;
CREATE TABLE cards (
  cardID VARCHAR(20),

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
  FOREIGN KEY (setID) REFERENCES sets ON DELETE SET NULL -- set added first, then the card. cards has FK, b/c it is 'many' in many-to-1 rel with sets
);

-- decks have 1-60 cards, and up to 4 duplicates
DROP TABLE IF EXISTS _cards_in_decks;
CREATE TABLE _cards_in_decks (
  userID int,
  deckID int,
  cardID varchar(20),
  count int, -- Using count variable allows duplicates, since it doesn't make the primary key refer to more than 1 row
             -- Count variable preferable to, e.g. deckSlot, since mixing insert/delete doesn't mess it up
 
  PRIMARY KEY (userID, deckID, cardID),
  FOREIGN KEY (deckID) REFERENCES decks, -- checks deck exists
  FOREIGN KEY (cardID) REFERENCES cards ON DELETE CASCADE-- checks card exists in collection
);

-- b/c there are multiple users, there are multiple collections. 
-- So so need a way to determine from all users' cards, which ones belong to a certain user
DROP TABLE IF EXISTS _cards_in_collections;
CREATE TABLE _cards_in_collections (
  userID int,
  cardID VARCHAR(20),
  count int,

  PRIMARY KEY (userID, cardID),
  FOREIGN KEY (cardID) REFERENCES cards ON DELETE CASCADE
);

-- extra pokemon info
DROP TABLE IF EXISTS pokemon;
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
  FOREIGN KEY (id) REFERENCES cards ON DELETE CASCADE -- inherits card info
);

-- create table attacks
DROP TABLE IF EXISTS attacks;
CREATE TABLE attacks (
  id VARCHAR(20),
  nameAttack varchar(55) NOT NULL,
  cost int,
  damage int,
  text varchar(555),
  PRIMARY KEY (id, nameAttack),
  FOREIGN KEY (id) REFERENCES pokemon ON DELETE CASCADE
);

-- create abilities table
DROP TABLE IF EXISTS abilities;
CREATE TABLE abilities (
  id VARCHAR(20),
  nameAbility varchar(55) NOT NULL,
  type varchar(55),
  text varchar(555),
  PRIMARY KEY (nameAbility),
  FOREIGN KEY (id) REFERENCES pokemon ON DELETE CASCADE
);

-- create weaknesses table
DROP TABLE IF EXISTS weaknesses;
CREATE TABLE weaknesses (
  id varchar(20),
  typeWeaknesses varchar(55),
  valueWeaknesses varchar(5), -- e.g. 1.5
  PRIMARY KEY (typeWeaknesses, valueWeaknesses),
  FOREIGN KEY (id) REFERENCES pokemon ON DELETE CASCADE
);

-- create resistance table
DROP TABLE IF EXISTS resistances;
CREATE TABLE resistances (
  id varchar(20),
  typeResistances varchar(55),
  valueResistances varchar(5), -- e.g. 0.5
  PRIMARY KEY (typeResistances, valueResistances),
  FOREIGN KEY (id) REFERENCES pokemon ON DELETE CASCADE
);

-------------------------------------
-- INITIALIZATION -------------------
-------------------------------------

-- Inserting some cards
-- There is a hiearachy to inserts; sets -> cards -> pokemon -> attacks, abilities, types
INSERT INTO sets VALUES
('swsh9', 'Sword & Shield Brilliant Stars', 'Sword & Shield Brilliant Stars', 172, 999, 'Legal', 'Banned', NULL, 'Blah', 'Blah', 'Blah', 
  'https://images.pokemontcg.io/swsh9/symbol.png', 'https://images.pokemontcg.io/swsh9/logo.png');
INSERT INTO cards VALUES 
('swsh9-87', 'Weavile', 'Pokemon', '{"Basic"}', '{"Darkness"}', '{"Rules go here"}', 
  'swsh9', 150, 'Hasuno', 'Common', 'Flavor Text', 'Legal', 'Banned', NULL,
  'F', 'https://images.pokemontcg.io/swsh9/87.png', 'https://images.pokemontcg.io/swsh9/87_hires.png');
INSERT INTO pokemon VALUES
('swsh9-87', 10, 100, 461, 'Sneasel', NULL);
INSERT INTO attacks VALUES
('swsh9-87', 'Ransack', 1, 0, 'Flip 2 coins. If either of them is heads, your opponent reveals their hand. 
  For each heads, choose a card you find there and put it on the bottom of your opponent’s deck in any order.'),
('swsh9-87', 'Slash', 3, 100, NULL);
INSERT INTO weaknesses VALUES 
('swsh9-87', 'Grass', '2');
-- no resistances
-- no abilities

INSERT INTO sets VALUES
('xy1', 'XY', 'XY', 146, 146, 'Legal', 'Legal', NULL, 'XY', '2014/02/05', '2018/03/04 10:35:00', 
  'https://images.pokemontcg.io/xy1/symbol.png', 'https://images.pokemontcg.io/xy1/logo.png');
INSERT INTO cards VALUES 
('xy1-1', 'Venusaur-EX', 'Pokemon', '{"Basic", "EX"}', '{"Grass"}', '{"Pokémon-EX rule: When a Pokémon-EX has been Knocked Out, your opponent takes 2 Prize cards."}', 
  'xy1', 1, 'Eske Yoshinob', 'Rare Holo EX', NULL, 'Legal', 'Legal', NULL,
  NULL, 'https://images.pokemontcg.io/xy1/1.png', 'https://images.pokemontcg.io/xy1/1_hires.png');
INSERT INTO pokemon VALUES
('xy1-1', 10, 180, 461, NULL, NULL);
INSERT INTO attacks VALUES
('xy1-1', 'Poison Powder', 3, 60, 'Your opponent''s Active Pokémon is now Poisoned.'),
('xy1-1', 'Jungle Hammer', 4, 90, 'Heal 30 damage from this Pokémon.');
INSERT INTO weaknesses VALUES 
('xy1-1', 'Fire', '2');
-- no resistances
-- no abilities

-- data from API call -- 
-- (Card(abilities=None, artist='Eske Yoshinob', ancientTrait=None, attacks=[Attack(name='Poison Powder', cost=['Grass', 'Colorless', 'Colorless'], convertedEnergyCost=3, damage='60', 
-- text="Your opponent's Active Pokémon is now Poisoned."), Attack(name='Jungle Hammer', cost=['Grass', 'Grass', 'Colorless', 'Colorless'], convertedEnergyCost=4, damage='90', 
-- text='Heal 30 damage from this Pokémon.')], cardmarket=Cardmarket(url='https://prices.pokemontcg.io/cardmarket/xy1-1', updatedAt='2022/10/26', 
-- prices=CardmarketPrices(averageSellPrice=5.25, lowPrice=1.99, trendPrice=5.91, germanProLow=None, suggestedPrice=None, reverseHoloSell=None, reverseHoloLow=None, 
-- reverseHoloTrend=4.37, lowPriceExPlus=3.0, avg1=5.0, avg7=6.02, avg30=5.51, reverseHoloAvg1=3.99, reverseHoloAvg7=4.56, reverseHoloAvg30=4.47)), convertedRetreatCost=4, 
-- evolvesFrom=None, flavorText=None, hp='180', id='xy1-1', images=CardImage(small='https://images.pokemontcg.io/xy1/1.png', large='https://images.pokemontcg.io/xy1/1_hires.png'), 
-- legalities=Legality(unlimited='Legal', expanded='Legal', standard=None), regulationMark=None, name='Venusaur-EX', nationalPokedexNumbers=[3], number='1', rarity='Rare Holo EX', 
-- resistances=None, retreatCost=['Colorless', 'Colorless', 'Colorless', 'Colorless'], rules=['Pokémon-EX rule: When a Pokémon-EX has been Knocked Out, your opponent takes 2 Prize cards.'], 
-- set=Set(id='xy1', images=SetImage(symbol='https://images.pokemontcg.io/xy1/symbol.png', logo='https://images.pokemontcg.io/xy1/logo.png'), 
-- legalities=Legality(unlimited='Legal', expanded='Legal', standard=None), name='XY', printedTotal=146, ptcgoCode='XY', releaseDate='2014/02/05', series='XY', total=146, 
-- updatedAt='2018/03/04 10:35:00'), subtypes=['Basic', 'EX'], supertype='Pokémon', tcgplayer=TCGPlayer(url='https://prices.pokemontcg.io/tcgplayer/xy1-1', 
-- updatedAt='2022/10/26', prices=TCGPrices(normal=None, holofoil=TCGPrice(low=2.4, mid=3.94, high=40.02, market=3.59, directLow=3.61), reverseHolofoil=None, 
-- firstEditionHolofoil=None, firstEditionNormal=None)), types=['Grass'], weaknesses=[Weakness(type='Fire', value='×2')])
-- )


