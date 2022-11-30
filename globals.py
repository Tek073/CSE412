# search for cards in some table, by various parameters
def search_cards(cur, tbl_name, conditions:dict):
    str = []
    str = ' AND '.join(cur.mogrify('%s = %s', key, conditions[key]) for key in conditions)
    cur.execute(f'''
        SELECT cardID
        FROM {tbl_name}
        WHERE ''' + str)
    return cur.fetchall()

def search(cur):
    cur.execute('''
    SELECT *
    FROM cards
    ''')
    return cur.fetchall()
    
# returns only necessary info to DISPLAY cards
# pass conds with cic. or c., depending on 
def collection_search(cur, conds):
    cols = ['cic.cardID','name','count','largeImage']
    tbls = ['_cards_in_collections cic','cards c']
    advanced_search(cur, cols, tbls, conds)

# Beware: make sure to specify tbl.col in kwargs if you search thru multiple tables
def advanced_search(cur, cols:list, tbls:list, conds:dict, **kwargs):
    s = []
    f = []
    w = []

    s = ', '.join(cur.mogrify('%s', col) for col in cols)
    f = ', '.join(cur.mogrify('%s', tbl) for tbl in tbls)
    w = ' AND '.join(cur.mogrify('%s = %s', key, conds[key]) for key in conds)

    execStr = '''
        SELECT ''' + s + '''
        FROM ''' + f + '''
        WHERE ''' + w
    # if kwargs.get("order") != None:
    #     execStr += 'ORDER BY ' + kwargs["order"]

    cur.execute(execStr)

    return cur.fetchall()
