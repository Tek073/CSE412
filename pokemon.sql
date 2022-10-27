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
  PRIMARY KEY (pxdx),
  FOREIGN KEY (nameAbility) REFERENCES abilities(nameAbility),
  FOREIGN KEY (nameAttack) REFERENCES attacks(nameAttack),
  FOREIGN KEY (typeWeaknesses, valueWeaknesses) REFERENCES weaknesses(typeWeaknesses, valueWeaknesses),
  FOREIGN KEY (typeResistances, valueResistances) REFERENCES resistances(typeResistances, valueResistances)
);

INSERT INTO pokemon
VALUES
  ('biddof', 12, 33, 1, 'barbarrel', 'n/a', 'harden', 'pound', 'fire', 2, 'water', 2);
  
SELECT * FROM pokemon
