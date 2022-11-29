CREATE TABLE "sets" (
  setID VARCHAR(20), -- e.g. "swsh1"

  name VARCHAR(55),
  series VARCHAR(55),
  printedTotal INT,
  total INT,

  stdLeg VARCHAR(10),
  expLeg VARCHAR(10),
  unlLeg VARCHAR(10),

  ptcgoCode VARCHAR(55),
  releaseDate VARCHAR(55),
  updatedAt VARCHAR(55),

  symbol VARCHAR(255),
  logo VARCHAR(255),

  PRIMARY KEY (setID)
  --FOREIGN KEY (setID) REFERENCES cards(setID)
);