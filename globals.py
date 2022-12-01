# search for cards in some table, by various parameters
def search_cards(cur, tbl_name, conditions:dict):
    str = []
    str = ' AND '.join(cur.mogrify('%s = %s', key, conditions[key]) for key in conditions)
    cur.execute(f'''
        SELECT cardID
        FROM {tbl_name}
        WHERE ''' + str)
    return cur.fetchall()

# def search(cur):
#     cur.execute('''
#     SELECT *
#     FROM cards
#     ''')
#     return cur.fetchall()
    
# # returns only necessary info to DISPLAY cards
# # pass conds with cic. or c., depending on 
# def collection_search(cur, conds):
#     cols = ['cic.cardID','name','count','largeImage']
#     tbls = ['_cards_in_collections cic','cards c']
#     advanced_search(cur, cols, tbls, conds)

# # Beware: make sure to specify tbl.col in kwargs if you search thru multiple tables
# def advanced_search(cur, cols:list, tbls:list, conds:dict, **kwargs):
#     s = []
#     f = []
#     w = []

#     s = ', '.join(cur.mogrify('%s', col) for col in cols)
#     f = ', '.join(cur.mogrify('%s', tbl) for tbl in tbls)
#     w = ' AND '.join(cur.mogrify('%s = %s', key, conds[key]) for key in conds)

#     execStr = '''
#         SELECT ''' + s + '''
#         FROM ''' + f + '''
#         WHERE ''' + w
#     # if kwargs.get("order") != None:
#     #     execStr += 'ORDER BY ' + kwargs["order"]

#     cur.execute(execStr)

#     return cur.fetchall()

# !!! assuming 'self' is Decks or Collection Object !!!
def advanced_search(self, conds:dict, **kwargs):
        cur = self.cursor
        d = ''
        
        arrConds = {}
        keys = ['subtypes','types','rules']
        for k in keys:
            if conds.get(k) != '':
                arrConds[k] = conds[k]
            del conds[k]
        print(arrConds)

        legConds = {}
        legs = ['unlLeg', 'expLeg', 'stdLeg']
        for leg in legs:
            if conds.get(leg) != None:
                if conds.get(leg) == 'Legal':
                    legConds[leg] = conds[leg]
                elif conds.get(leg) == 'Illegal':
                    legConds[leg] = None
                del conds[leg]
        print(conds)

        temp = dict(conds) # create copy of data, so we can delete key-value pairs during iteration
        for key in temp:
            if temp[key] == '':
                del conds[key]

        print(conds)
        print(legConds)
        if kwargs.get('deckID') != None:
            d = 'AND ' + '(' + ' OR '.join((cur.mogrify('deckID = %s', id)).decode() for id in kwargs['deckID']) + ')'
        w = ''.join(cur.mogrify(' AND upper(%s) LIKE upper(%%s)' % key, ['%'+conds[key]+'%']).decode() for key in conds)
        a = ''.join(cur.mogrify(' AND %s @> %%s::varchar[]' % key, [arrConds[key].split(',')]).decode() for key in arrConds)
        l = ''.join(cur.mogrify(' AND %s = %%s' % key, [legConds[key]]).decode() for key in legConds)
        print(d+a+w+l)

        # assuming 'self' is Decks or Collection
        id = self.userID[0]

        if kwargs.get('search_in') != None:
            if kwargs['search_in'] == 'decks':
                cur.execute(f'''
                    SELECT cid.cardID, name, count, largeImage  
                    FROM _cards_in_decks cid, cards c
                    WHERE userID = {id} AND cid.cardID = c.cardID''' + d + w + a + l)
            if kwargs['search_in'] == 'collection':
                cur.execute(f'''
                    SELECT cic.cardID, name, smallImage, largeImage, types  
                    FROM _cards_in_collection cic, cards c
                    WHERE userID = {id} AND cic.cardID = c.cardID''' + d + w + a + l)
            if kwargs['search_in'] == 'cards':
                cur.execute(f'''
                    SELECT cardID, name, smallImage, largeImage, types  
                    FROM cards c
                    WHERE userID = {id}''' + d + w + a + l)

        to_return = cur.fetchall()
        print (to_return)
        return to_return
