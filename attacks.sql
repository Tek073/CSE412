CREATE TABLE attacks (
  name varchar(55) NOT NULL,
  cost int,
  text varchar(55),
  damage int,
  PRIMARY KEY (name)
);

INSERT INTO attacks
VALUES ('tackle', 2, 'charge the opponent', 20);
VALUES ('pound', 2, 'pound the pokemon', 30);
VALUES ('scratch', 1, 'scratch the pokemon', 25);

SELECT * FROM attacks;
