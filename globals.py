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

# !!! assuming 'self' is Decks, Collection or User Object !!!
def advanced_search(self, conds:dict, **kwargs):
        cur = self.cursor
        try:
            id = self.userID[0] # Decks and Collection
        except:
            id = self.id[0] # User
        d = ''
        
        arrConds = {}
        keys = ['subtypes','types','rules']
        for k in keys:
            if conds.get(k) != '' and conds.get(k) != None:
                arrConds[k] = conds[k].strip()
            try:
                del conds[k]
            except:
                print('key error for arrConds')
                pass
        print("arrConds:",arrConds)

        legConds = {}
        legs = ['unlLeg', 'expLeg', 'stdLeg']
        for leg in legs:
            if conds.get(leg) != None:
                if conds.get(leg) == 'Legal':
                    legConds[leg] = conds[leg].strip()
                elif conds.get(leg) == 'Illegal':
                    legConds[leg] = None
                del conds[leg]
        print("legConds:",legConds)

        print("conds before deletion:",conds)
        temp = dict(conds) # create copy of data, so we can delete key-value pairs during iteration
        for key in temp:
            if temp[key] == '':
                del conds[key]
            else:
                conds[key] = temp[key].strip()
        print("conds after deletion:",conds)
        
        if kwargs.get('deckID') != None:
            did = kwargs['deckID']
            d = ' AND ' + '(' + ((cur.mogrify(f'deckID = {did}')).decode()) + ')'
        w = ''.join(cur.mogrify(' AND upper(%s) LIKE upper(%%s)' % key, ['%'+conds[key]+'%']).decode() for key in conds)
        #a = ''.join(cur.mogrify(' AND %s @> %%s::varchar[]' % key, [arrConds[key].split(',')]).decode() for key in arrConds)
        
        a = ''.join(''.join(cur.mogrify('''
         AND EXISTS (
        SELECT 1 FROM unnest(%s) AS a
        WHERE upper(a) LIKE upper(%%s))''' 
        % key, ['%'+i.strip()+'%']).decode() for i in arrConds[key].split(',')) 
        for key in arrConds)

        l = ''.join(cur.mogrify(' AND %s = %%s' % key, [legConds[key]]).decode() for key in legConds)

        print("full mogrified string:",d+a+w+l)

        if kwargs.get('search_in') != None:
            if kwargs['search_in'] == 'decks':
                cur.execute(f'''
                    SELECT cid.cardID, name, smallImage, largeImage, types, count  
                    FROM _cards_in_decks cid, cards c
                    WHERE userID = {id} AND cid.cardID = c.cardID''' + d + w + a + l)
            if kwargs['search_in'] == 'collection':
                cur.execute(f'''
                    SELECT cic.cardID, name, smallImage, largeImage, types, count  
                    FROM _cards_in_collections cic, cards c
                    WHERE userID = {id} AND cic.cardID = c.cardID''' + d + w + a + l)
            if kwargs['search_in'] == 'cards':
                cur.execute(f'''
                    SELECT cardID, name, smallImage, largeImage, types, setID
                    FROM cards c
                    WHERE 0=0''' + d + w + a + l) # 0=0, to account for first 'AND' in dwal, 
                                                # setID just to match col counts

        to_return = cur.fetchall()
        print (to_return)
        return to_return
