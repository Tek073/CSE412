# search for cards in some table, by various parameters
def search_cards(cur, tbl_name, **kwargs):
    str = []
    ' AND '.join(cur.mogrify('%s = %s', key, kwargs[key]) for key in kwargs)
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
