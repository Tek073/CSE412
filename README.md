# CSE412
412-repository for group project <br/>
Things people are working on <br/>

Ryan - n/a <br/>
Luc - Card, Set, Collections, User, Deck <br/>
-- I'm changing pokemon. Right now, it has FK references to attacks, abilities etc. But this makes it so those attacks, abilities are built-in to
   pokemon table, which would result in redundant info if pokemon has multiple items. I'm changing it so that FK references are in attacks, abilites etc.
   tables instead. <br/>
-- I simplified ER -> Relational conversion. Cards are now the user's collection; no separate collection table. Cards also have a count now. <br/>
-- ~~Removing resistances, weaknesses table and putting them in pokemon. Since res/weak tables' primary keys are all of their attributes, there is no point in having them.~~ Never mind, could be more than one resistances or weaknesses, though I have not personally seen an example of that yet.

In Progress - <br/>
Finished Work - attack, abilities, resistence, weakness, pokemon <br/>
Also a test for the pokemon has a relationship has been tested <br/>
Legalities and the relationship with primary key were added to pokemonHasATest file <br/>

Trainer/Energy (reliant on a card class) <br/>


