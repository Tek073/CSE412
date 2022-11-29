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
RestClient.configure('') # API key goes here

# if given setID, finds set and adds to 'Sets' table. If given set object, just adds it
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

# Get all cards from API, and add to 'Sets' table
def updateSetsTable(user):
    cur = user.cursor
    setStr = []

    sets = Set.all()

    for s in sets:
        setInfo = [s.id, s.name, s.series, s.printedTotal, s.total,
                    s.legalities.unlimited, s.legalities.expanded, s.legalities.standard,
                    s.ptcgoCode, s.releaseDate, s.updatedAt, s.images.symbol, s.images.logo]

        setStr.append(f'{setInfo}'[1:-1]) # remove brackets []
        i += 1

    argsStr = ','.join(cur.mogrify("(%s)", s) for s in setStr)
    user.cursor.execute('''INSERT INTO sets VALUES ''' + argsStr)

# Get all cards from API, and add to 'Cards' table
def updateCardTable(user):
    cur = user.cursor
    cardStr = []
    pokemonStr = []
    attackStr = []
    abilityStr = []
    weaknessStr = []
    resistanceStr = []

    cards = Card.all()

    for c in cards:

        cardInfo = \
        [c.id, c.name, c.supertype, c.subtypes, c.types, c.rules,
        c.set.id, c.number, c.artist, c.rarity, c.flavorText,
        c.legalities.unlimited, c.legalities.expanded, c.legalities.standard,
        c.regulationMark, c.images.small, c.images.large]

        cardStr.append(f'{cardInfo}'[-1:1])

        if (c.supertype == 'Pokémon'): # Beware the accent aigu (é)
            pokemonInfo = \
            [c.id, c.level, c.hp, c.nationalPokedexNumbers, c.evolvesFrom, c.evolvesTo]
            # todo: pokedex# is actually an array. Also, evolvesTo might not be present    
            pokemonStr.append(f'{pokemonInfo}'[1:-1])
        
            for a in c.attacks:
                attacksInfo = \
                [c.id, a.name, a.convertedEnergyCost, a.damage, a.text]
                attackStr.append(f'{attacksInfo}'[1:-1])

            for ab in c.abilities:
                abilityInfo = \
                [c.id, ab.name, ab.type, ab.text]
                abilityStr.append(f'{abilityInfo}'[1:-1])

            for w in c.weaknesses:
                weaknessInfo = \
                [c.id, w.type, w.value]
                weaknessStr.append(f'{weaknessInfo}'[1:-1])

            for r in c.resistances:
                resistanceInfo = \
                [c.id, r.type, r.value]
                resistanceStr.append(f'{resistanceInfo}'[1:-1])

    argsStr = ','.join(cur.mogrify("(%s)", str) for str in cardStr)
    cur.execute('''INSERT INTO cards VALUES ''' + argsStr)

    argsStr = ','.join(cur.mogrify("(%s)", str) for str in pokemonStr)
    cur.execute('''INSERT INTO pokemon VALUES ''' + argsStr)

    argsStr = ','.join(cur.mogrify("(%s)", str) for str in attackStr)
    cur.execute('''INSERT INTO attacks VALUES ''' + argsStr)

    argsStr = ','.join(cur.mogrify("(%s)", str) for str in abilityStr)
    cur.execute('''INSERT INTO abilities VALUES ''' + argsStr)

    argsStr = ','.join(cur.mogrify("(%s)", str) for str in weaknessStr)
    cur.execute('''INSERT INTO weaknesses VALUES ''' + argsStr)

    argsStr = ','.join(cur.mogrify("(%s)", str) for str in resistanceStr)
    cur.execute('''INSERT INTO resistances VALUES ''' + argsStr)

# if given cardID, finds card and adds to 'Cards' table. If given card object, just adds it
def addIfNewCard(user, **kwargs):
    keys = kwargs.keys
    cardID = []

    if keys.get("name"):
        cards = Card.where(q=f'card.name:{keys["name"]}')
        cardID.append((card.id for card in cards))

    elif keys.get("cardID"):
        cards = Card.find(f'{keys["cardID"]}')
        cardID.append(cards.id)

        user.cursor.execute('''
            SELECT *
            FROM cards
            WHERE cards.cardID = %s;''',
            (cardID)
        )
        if (user.cursor.fetchall() != None): 
            return    

    for c in cards:
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
