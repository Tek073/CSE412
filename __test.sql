------------------------
-- TEST QUERIES --------
------------------------

INSERT INTO users VALUES
(1, 'asdf', 'asdf');

INSERT INTO decks VALUES
(1, 1234, 'my-deck')

INSERT INTO _cards_in_collections VALUES
(1, 'swsh9-87', 1)
INSERT INTO _cards_in_decks VALUES
(1, 1234, 'swsh9-87', 1)

INSERT INTO _cards_in_collections VALUES
(1, 'xy1-1', 10)
INSERT INTO _cards_in_decks VALUES
(1, 1234, 'xy1-1', 4)