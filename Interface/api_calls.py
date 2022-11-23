import sys
import psycopg2
from psycopg2 import Error
from psycopg2 import *

from pokemontcgsdk import Card
from pokemontcgsdk import Set
from pokemontcgsdk import Type
from pokemontcgsdk import Supertype
from pokemontcgsdk import Subtype
from pokemontcgsdk import Rarity

from pokemontcgsdk import RestClient
RestClient.configure('92e6be5e-7d21-4d3e-9900-1753c97c0979') # API key goes here

def addNewSet(user, setID):
        s = Set.find(setID)

        setInfo = [s.id, s.name, s.series, s.printedTotal, s.total,
                    s.legalities.unlimited, s.legalities.expanded, s.legalities.standard,
                    s.ptcgoCode, s.releaseDate, s.updatedAt, s.images.symbol, s.images.logo]

        setStr = f'{setInfo}'[1:-1] # remove brackets []
        user.cursor.execute('''
            INSERT INTO sets
            VALUES (%s);''',
            (setStr,)
        )

def addIfNewCard(user, cardID):
    # check if card exists in 'cards'
    user.cursor.execute('''
        SELECT *
        FROM cards
        WHERE cards.cardID = %s;''',
        (cardID,)
    )
    if (user.cursor.fetchall() != None): 
        return    

    c = Card.find(cardID)
    # check if card's set is in 'sets'
    setID = c.set.id
    user.cursor.execute('''
        SELECT *
        FROM sets
        WHERE sets.setID = %s;''',
        (setID,)
    )
    if (user.cursor.fetchall() == None): 
        user.addNewSet(setID)

    # create card info, which contains info common to all card supertypes
    cardInfo = \
    [c.id, c.name, c.supertype, c.subtypes, c.types, c.rules,
    c.set.id, c.number, c.artist, c.rarity, c.flavorText,
    c.legalities.unlimited, c.legalities.expanded, c.legalities.standard,
    c.regulationMark, c.images.small, c.images.large]

    cardString = f'{cardInfo}'[-1:1]

    user.cursor.execute('''
        INSERT INTO cards
        VALUES (%s);''',
        (cardString,)
    )

    # btw, energy and trainer cards do not need anything extra. Just pokemon
    if (c.supertype == 'Pokémon'): # Beware the accent aigu (é)
        pokemonInfo = \
        [c.id, c.level, c.hp, c.nationalPokedexNumbers, c.evolvesFrom, c.evolvesTo]
        # todo: pokedex# is actually an array. Also, evolvesTo might not be present
        
        pokemonString = f'{pokemonInfo}'[1:-1]
        user.cursor.execute('''
            INSERT INTO pokemon
            VALUES (%s);''',
            (pokemonString,)
        )

        # the following info, some pkmn have multiple of. 
        # So instead of putting directly in pkmn table, put in other tables
        for a in c.attacks:
            attacksInfo = \
            [c.id, a.name, a.convertedEnergyCost, a.damage, a.text]
            attackStr = f'{attacksInfo}'[1:-1]
            user.cursor.execute('''
                INSERT INTO attacks
                VALUES (%s);''',
                (attackStr,)
            )

        for ab in c.abilities:
            abilityInfo = \
            [c.id, ab.name, ab.type, ab.text]
            abilityStr = f'{abilityInfo}'[1:-1]
            user.cursor.execute('''
                INSERT INTO abilities
                VALUES (%s);''',
                (abilityStr,)
            )

        for w in c.weaknesses:
            weaknessInfo = \
            [c.id, w.type, w.value]
            weaknessStr = f'{weaknessInfo}'[1:-1]
            user.cursor.execute('''
                INSERT INTO weaknesses
                VALUES (%s);''',
                (weaknessStr,)
            )

        for r in c.resistances:
            resistanceInfo = \
            [c.id, r.type, r.value]
            resistanceStr = f'{resistanceInfo}'[1:-1]
            user.cursor.execute('''
                INSERT INTO resistances
                VALUES (%s);''',
                (resistanceStr,)
            )
