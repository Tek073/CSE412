CREATE TABLE pokemon (
  namePokemon varchar(55),
  level int,
  hp int,
  pxdx int,
  evolvesTo varchar(55),
  evolvesFrom varchar(55),
  nameAbility varchar(55),
  PRIMARY KEY (pxdx),
  FOREIGN KEY (nameAbility) REFRENCES abilities(nameAbility)
);

INSERT INTO pokemon
VALUES
  ('biddof', 12, 33, 1, 'barbarrel', 'n/a', 'harden');
  
SELECT * FROM pokemon
