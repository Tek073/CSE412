------------------------
-- TEST QUERIES --------
------------------------

INSERT INTO users 
VALUES
(1, 'asdf', 'asdf'),
(2, 'pokemaster', '123'),
(3, 'ryan', 'mypass'),
(4, 'jason', 'lol21'),
(5, 'sihno master', 'biddof'),
(6, 'yooyyoy', 'a password'),
(7, 'hi', 'sf071'),
(8, 'brock', '1rj1013'),
(9, 'ash', 'jslkf213'),
(10, 'yoyoyo', 'f10f11280');

INSERT INTO decks VALUES
(1, 1234, 'my-deck');

INSERT INTO _cards_in_collections VALUES
(2, 'swsh9-87', 1);
INSERT INTO _cards_in_decks VALUES
(1, 1234, 'swsh9-87', 1);

INSERT INTO _cards_in_collections VALUES
(1, 'xy1-1', 10);
INSERT INTO _cards_in_decks VALUES
(1, 1234, 'xy1-1', 4);

SELECT * FROM users
