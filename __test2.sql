
INSERT INTO users VALUES
(1, 'asdf', 'asdf'),
(2, 'pokemaster', '123'),
(3, 'ryan', 'mypass'),
(4, 'jason', 'lol21'),
(5, 'sihno master', 'biddof');

-- notice that users 3 4 do not have decks
INSERT INTO decks VALUES
(1, 1234, 'my-deck'),
(1, 5678, 'my-deck2'),
(2, 8911, 'pokemasterDeck'),
(2, 190, 'pokemasterDeck2'),
(5, 1511, 'sihnoDeckBest');

INSERT INTO sets VALUES
('a1', 'Sword & Shield Brilliant Stars', 'Sword & Shield Brilliant Stars', 172, 999, 'Legal', 'Banned', NULL, 'Blah', 'Blah', 'Blah', 
  'https://images.pokemontcg.io/swsh9/symbol.png', 'https://images.pokemontcg.io/swsh9/logo.png'),
('a2', 'Diamond & Peral Sinnohs Revenge', 'Diamond & Peral Sihnos Revenge', 173, 999, 'Legal', 'Banned', NULL, 'Blah', 'Blah', 'Blah', 
  'https://images.pokemontcg.io/swsh9/symbol.png', 'https://images.pokemontcg.io/swsh9/logo.png');
  
INSERT INTO cards VALUES 
('10', 'Charmandar', 'Pokemon', '{"Basic"}', '{"Fire"}', '{"Rules go here"}', 
  'a1', 150, 'Hasuno', 'Rare', 'Flavor Text', 'Legal', 'Banned', NULL,
  'F', 'https://images.pokemontcg.io/swsh9/87.png', 'https://images.pokemontcg.io/swsh9/87_hires.png'),
('11', 'Biddof', 'Pokemon', '{"Basic"}', '{"Normal"}', '{"Rules go here"}', 
  'a1', 150, 'Hasuno', 'Rare', 'Flavor Text', 'Legal', 'Banned', NULL,
  'F', 'https://images.pokemontcg.io/swsh9/87.png', 'https://images.pokemontcg.io/swsh9/87_hires.png'),
('12', 'Stunky', 'Pokemon', '{"Basic"}', '{"Dark","Poison"}', '{"Rules go here"}', 
  'a1', 150, 'Hasuno', 'Rare', 'Flavor Text', 'Legal', 'Banned', NULL,
  'F', 'https://images.pokemontcg.io/swsh9/87.png', 'https://images.pokemontcg.io/swsh9/87_hires.png'),
('13', 'Meditite', 'Pokemon', '{"Basic"}', '{"Fight","Phycic"}', '{"Rules go here"}', 
  'a1', 150, 'Hasuno', 'Common', 'Flavor Text', 'Legal', 'Banned', NULL,
  'F', 'https://images.pokemontcg.io/swsh9/87.png', 'https://images.pokemontcg.io/swsh9/87_hires.png'),
('14', 'Whiscash', 'Pokemon', '{"Basic"}', '{"Water","Ground"}', '{"Rules go here"}', 
  'a2', 150, 'Hasuno', 'Common', 'Flavor Text', 'Legal', 'Banned', NULL,
  'F', 'https://images.pokemontcg.io/swsh9/87.png', 'https://images.pokemontcg.io/swsh9/87_hires.png'),
('15', 'Gastly', 'Pokemon', '{"Basic"}', '{"Poison","Ghost"}', '{"Rules go here"}', 
  'a2', 150, 'Hasuno', 'Super Rare', 'Flavor Text', 'Legal', 'Banned', NULL,
  'F', 'https://images.pokemontcg.io/swsh9/87.png', 'https://images.pokemontcg.io/swsh9/87_hires.png'),
('16', 'Lopunny', 'Pokemon', '{"Basic"}', '{"Normal"}', '{"Rules go here"}', 
  'a2', 150, 'Hasuno', 'Super Rare', 'Flavor Text', 'Legal', 'Banned', NULL,
  'F', 'https://images.pokemontcg.io/swsh9/87.png', 'https://images.pokemontcg.io/swsh9/87_hires.png'),
('17', 'Starly', 'Pokemon', '{"Basic"}', '{"Flying","Normal"}', '{"Rules go here"}', 
  'a2', 150, 'Hasuno', 'Common', 'Flavor Text', 'Legal', 'Banned', NULL,
  'F', 'https://images.pokemontcg.io/swsh9/87.png', 'https://images.pokemontcg.io/swsh9/87_hires.png');

INSERT INTO pokemon VALUES
('10', 10, 100, 461, 'Charmander', NULL),
('11', 12, 80, 444, 'Biddof', NULL),
('12', 15, 110, 554, 'biddof', NULL),
('13', 16, 110, 151, 'Medidite', NULL),
('14', 10, 100, 461, 'Whiscash', NULL),
('15', 12, 80, 444, 'Gastly', NULL),
('16', 15, 110, 554, 'Lopunny', NULL),
('17', 16, 110, 151, 'Starly', NULL);

-- INSERT INTO _cards_in_collection VALUES
-- note that each collection or deck must belong to a user
INSERT INTO _cards_in_collections VALUES
(2, '11', 1);

INSERT INTO _cards_in_decks VALUES
(1, 1234, '11', 1);

INSERT INTO _cards_in_collections VALUES
(1, '12', 10);

INSERT INTO _cards_in_decks VALUES
(1, 1234, '12', 4);

-- only take userID 1 decks and show decks name and id
SELECT cards.rarity, cards.name
FROM cards
WHERE cards.rarity='Common';
