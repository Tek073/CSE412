import sys
import psycopg2
from psycopg2 import Error
from psycopg2 import *
import time

from pokemontcgsdk import Card
from pokemontcgsdk import Set
from pokemontcgsdk import Type
from pokemontcgsdk import Supertype
from pokemontcgsdk import Subtype
from pokemontcgsdk import Rarity

from pokemontcgsdk import RestClient
RestClient.configure('92e6be5e-7d21-4d3e-9900-1753c97c0979') # API key goes here

def create_value(cur, list):
    return cur.mogrify('(' + '%s, '*(len(list)-1) + '%s)', list).decode()

# unfortunately, you can't simply update all columns. You have to hardcode all cols you want updated. 
# I figure cards probably don't have to be updated that often, so it's fine to simply DO NOTHING
# Besides, if we want to update, we can delete and re-add
# def create_upsert(tbl_name, values, conflict):
#     return (f'INSERT INTO {tbl_name} VALUES {values} ON CONFLICT {conflict} DO UPDATE.......')

def create_insert(tbl_name, values, conflict):
    return (f'INSERT INTO {tbl_name} VALUES {values} ON CONFLICT {conflict} DO NOTHING')

def create_card_inserts(argsStr):
    query = []
    query.append(create_insert('cards', argsStr[0], '(cardID)'))
    query.append(create_insert('pokemon', argsStr[1], '(cardID)'))
    query.append(create_insert('attacks', argsStr[2], '(cardID, name)'))
    query.append(create_insert('abilities', argsStr[3], '(cardID, name)'))
    query.append(create_insert('weaknesses', argsStr[4], '(cardID, type, value)'))
    query.append(create_insert('resistances', argsStr[5], '(cardID, type, value)'))
    return query

# Get all cards from API, and add to 'Sets' table
def updateSetsTable(conn):
    start_time = time.time()
    cur = conn.cursor()

    setStr = []
    sets = Set.all()

    for s in sets:
        setInfo = [s.id, s.name, s.series, s.printedTotal, s.total,
                    s.legalities.unlimited, s.legalities.expanded, s.legalities.standard,
                    s.ptcgoCode, s.releaseDate, s.updatedAt, s.images.symbol, s.images.logo]

        setStr.append(create_value(cur, setInfo)) # remove brackets []

    argsStr = ',\n'.join(setStr)

    original_stdout = sys.stdout 
    with open('all_sets.txt', 'w', encoding='utf-8') as f:
        sys.stdout = f 
        print(argsStr)
        sys.stdout = original_stdout 
        exit

    cur.execute(create_insert('sets', argsStr, '(setID)'))
    conn.commit()
    # cur.execute('''SELECT * FROM sets''')
    # print(cur.fetchall())

    print("--- %s seconds ---" % (time.time() - start_time))

# Get all cards from API, and add to 'Cards' table
def updateCardsTable(conn):
    start_time = time.time()
    cur = conn.cursor()

    cardStr = []
    pokemonStr = []
    attackStr = []
    abilityStr = []
    weaknessStr = []
    resistanceStr = []
    #cards = Card.where(q='set.name:generations')
    cards = Card.all()

    orig_stdout = sys.stdout
    f = open("all_cards_raw.txt", 'w', encoding='utf-8')
    sys.stdout = f
    print(cards)
    f.close
    sys.stdout = orig_stdout

    for c in cards:

        cardInfo = \
        [c.id, c.name, c.supertype, c.subtypes, c.types, c.rules,
        c.set.id, c.number, c.artist, c.rarity, c.flavorText,
        c.legalities.unlimited, c.legalities.expanded, c.legalities.standard,
        c.regulationMark, c.images.small, c.images.large]

        cardStr.append(create_value(cur, cardInfo))

        if (c.supertype == 'Pokémon'): # Beware the accent aigu (é)
            if not (hasattr(c, 'level')): c.level=None
            if not (hasattr(c, 'evolvesFrom')): c.evolvesFrom=None
            if not (hasattr(c, 'evolvesTo')): c.evolvesTo=None
            pokemonInfo = \
            [c.id, c.level, c.hp, c.nationalPokedexNumbers, c.evolvesFrom, c.evolvesTo]
            pokemonStr.append(create_value(cur, pokemonInfo))
        
            if c.attacks != None:
                for a in c.attacks:
                    attacksInfo = \
                    [c.id, a.name, a.cost, a.convertedEnergyCost, a.damage, a.text]
                    attackStr.append(create_value(cur, attacksInfo))

            if c.abilities != None:
                for ab in c.abilities:
                    abilityInfo = \
                    [c.id, ab.name, ab.type, ab.text]
                    abilityStr.append(create_value(cur, abilityInfo))

            if c.weaknesses != None:
                for w in c.weaknesses:
                    weaknessInfo = \
                    [c.id, w.type, w.value]
                    weaknessStr.append(create_value(cur, weaknessInfo))

            if c.resistances != None:
                for r in c.resistances:
                    resistanceInfo = \
                    [c.id, r.type, r.value]
                    resistanceStr.append(create_value(cur, resistanceInfo))

    argsStr = []
    argsStr.append(',\n'.join(cardStr))
    argsStr.append(',\n'.join(pokemonStr))
    argsStr.append(',\n'.join(attackStr))
    argsStr.append(',\n'.join(abilityStr))
    argsStr.append(',\n'.join(weaknessStr))
    argsStr.append(',\n'.join(resistanceStr))

    orig_stdout = sys.stdout
    with open('all_cards.txt', 'w', encoding='utf-8') as f:
        sys.stdout = f
        print('\n\n'.join(argsStr))
        sys.stdout = orig_stdout
        exit

    queries = create_card_inserts(argsStr)
    i = 0
    try:
        for query in queries:
            i += 1
            cur.execute(query) 
            conn.commit()
    except Exception as e:
        print(e)
        print(f"Query {i} messed up")

    conn.commit()

    print("--- %s seconds ---" % (time.time() - start_time))

# # if given setID, finds set and adds to 'Sets' table. If given set object, just adds it
# def addNewSet(conn, setID):
#         s = Set.find(setID)

#         setInfo = [s.id, s.name, s.series, s.printedTotal, s.total,
#                     s.legalities.unlimited, s.legalities.expanded, s.legalities.standard,
#                     s.ptcgoCode, s.releaseDate, s.updatedAt, s.images.symbol, s.images.logo]

#         setStr = f'{setInfo}'[1:-1] # remove brackets []
#         conn.cursor.execute('''
#             INSERT INTO sets
#             VALUES (%s);''',
#             (setStr,)
#         )

# # if given cardID, finds card and adds to 'Cards' table. If given card object, just adds it
# def addIfNewCard(conn, **kwargs):
#     keys = kwargs.keys
#     cardID = []

#     if keys.get("name"):
#         cards = Card.where(q=f'card.name:{keys["name"]}')
#         cardID.append((card.id for card in cards))

#     elif keys.get("cardID"):
#         cards = Card.find(f'{keys["cardID"]}')
#         cardID.append(cards.id)

#         conn.cursor.execute('''
#             SELECT *
#             FROM cards
#             WHERE cards.cardID = %s;''',
#             (cardID)
#         )
#         if (conn.cursor.fetchall() != None): 
#             return    

#     for c in cards:
#         # check if card's set is in 'sets'
#         setID = c.set.id
#         conn.cursor.execute('''
#             SELECT *
#             FROM sets
#             WHERE sets.setID = %s;''',
#             (setID,)
#         )
#         if (conn.cursor.fetchall() == None): 
#             conn.addNewSet(setID)

#         # create card info, which contains info common to all card supertypes
#         cardInfo = \
#         [c.id, c.name, c.supertype, c.subtypes, c.types, c.rules,
#         c.set.id, c.number, c.artist, c.rarity, c.flavorText,
#         c.legalities.unlimited, c.legalities.expanded, c.legalities.standard,
#         c.regulationMark, c.images.small, c.images.large]

#         cardString = f'{cardInfo}'[-1:1]

#         conn.cursor.execute('''
#             INSERT INTO cards
#             VALUES (%s);''',
#             (cardString,)
#         )

#         # btw, energy and trainer cards do not need anything extra. Just pokemon
#         if (c.supertype == 'Pokémon'): # Beware the accent aigu (é)
#             pokemonInfo = \
#             [c.id, c.level, c.hp, c.nationalPokedexNumbers, c.evolvesFrom, c.evolvesTo]
#             # todo: pokedex# is actually an array. Also, evolvesTo might not be present
            
#             pokemonString = f'{pokemonInfo}'[1:-1]
#             conn.cursor.execute('''
#                 INSERT INTO pokemon
#                 VALUES (%s);''',
#                 (pokemonString,)
#             )

#             # the following info, some pkmn have multiple of. 
#             # So instead of putting directly in pkmn table, put in other tables
#             for a in c.attacks:
#                 attacksInfo = \
#                 [c.id, a.name, a.cost, a.convertedEnergyCost, a.damage, a.text]
#                 attackStr = f'{attacksInfo}'[1:-1]
#                 conn.cursor.execute('''
#                     INSERT INTO attacks
#                     VALUES (%s);''',
#                     (attackStr,)
#                 )

#             for ab in c.abilities:
#                 abilityInfo = \
#                 [c.id, ab.name, ab.type, ab.text]
#                 abilityStr = f'{abilityInfo}'[1:-1]
#                 conn.cursor.execute('''
#                     INSERT INTO abilities
#                     VALUES (%s);''',
#                     (abilityStr,)
#                 )

#             for w in c.weaknesses:
#                 weaknessInfo = \
#                 [c.id, w.type, w.value]
#                 weaknessStr = f'{weaknessInfo}'[1:-1]
#                 conn.cursor.execute('''
#                     INSERT INTO weaknesses
#                     VALUES (%s);''',
#                     (weaknessStr,)
#                 )

#             for r in c.resistances:
#                 resistanceInfo = \
#                 [c.id, r.type, r.value]
#                 resistanceStr = f'{resistanceInfo}'[1:-1]
#                 conn.cursor.execute('''
#                     INSERT INTO resistances
#                     VALUES (%s);''',
#                     (resistanceStr,)
#                 )
