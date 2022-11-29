INSERT INTO sets VALUES
('bw10', 'Plasma Black', 'Black and White', 101, 105, 'Legal', 'Legal', NULL, 'Blah', 'Blah', 'Blah', 
  'https://images.pokemontcg.io/bw10/symbol.png', 'https://images.pokemontcg.io/bw10/logo.png');
  
INSERT INTO cards VALUES
('bw10-5', 'Tropius', 'Pokemon', '{Basic}', '{Grass}', '{Rules go here}', 'bw10', 5, 'Shigenori Negishi', 'Uncommon',
	'It flies by flapping its broad leaves and gives the sweet, delicious fruit around its neck to children.',
	'legal', 'legal', NULL, NULL,
 	'https://images.pokemontcg.io/bw10/5.png', 'https://images.pokemontcg.io/bw10/5_hires.png');

INSERT INTO pokemon VALUES
('bw10-5', NULL, 100, 357,NULL, NULL);

INSERT INTO attacks VALUES
('bw10-5', 'Return', 1, 10, 'Draw cards until you have 6 cards in your hand.'),
('bw10-5', 'Energy Press', 2, 20, 'Does 20 more damage for each Energy attached to the Defending Pokémon.');

INSERT INTO weaknesses VALUES
('bw10-5', 'Lightning', 2);

SELECT cards.name, cards.flavortext
FROM cards
WHERE cards.types @> ARRAY['Grass']::varchar[]
