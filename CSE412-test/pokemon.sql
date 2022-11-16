CREATE TABLE pokemon (
  id int,-- namePokemon varchar(55) unnecessary; primary key inherited from card
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
  PRIMARY KEY (id),
  FOREIGN KEY (id) REFERENCES cards(id), -- inherits card info
  FOREIGN KEY (nameAbility) REFERENCES abilities(nameAbility),
  FOREIGN KEY (nameAttack) REFERENCES attacks(nameAttack),
  FOREIGN KEY (typeWeaknesses, valueWeaknesses) REFERENCES weaknesses(typeWeaknesses, valueWeaknesses),
  FOREIGN KEY (typeResistances, valueResistances) REFERENCES resistances(typeResistances, valueResistances)
);

INSERT INTO pokemon
VALUES
  (0, 12, 33, 1, 'barbarrel', NULL, 'harden', 'pound', 'fire', 2, 'water', 2); -- instead of 'n/a', use NULL 
  
SELECT * FROM pokemon
