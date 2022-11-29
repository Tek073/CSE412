def search_cards(cur, tbl_name, **kwargs):
    str = []
    ' AND '.join(cur.mogrify('%s = %s', key, kwargs[key]) for key in kwargs)
    cur.execute(f'''
        SELECT cardID
        FROM {tbl_name}
        WHERE ''' + str)
    return cur.fetchall()