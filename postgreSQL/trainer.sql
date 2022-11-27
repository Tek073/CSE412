-- create energy trainer
CREATE TABLE trainer (
  name varchar(55),
  text varchar(100),
  -- id is dependent on card table existing
  id int NOT NULL REFERENCES cards(id),
  PRIMARY KEY(id)
);

-- assuming that id of trainer cards are 60 - 69
INSERT INTO trainer
VALUES
  ('Leon', 'Leon allows the drawing of 2 energy cards', 60),
  ('Lady', 'Lady does lady stuff. cool!', 61),
  ('Spark', 'Power up all electric attacks by x1.5', 62),
  ('Misty', 'Create mist. accuracy of enemy pokemon decreases', 63),
  ('Ash', 'Draw 1 random card', 64),
  ('Brock', 'Draw 2 random cards', 65),
  ('Professor Oak', 'Recall all pokemon', 66),
  ('Gym Trainer', 'Learn about pokemon', 67),
  ('Leon', 'Leon allows the drawing of 2 energy cards', 68),
  ('Misty', 'Create mist. accuracy of enemy pokemon decreases', 69);
