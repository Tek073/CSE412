# import sys
# from os import path
# sys.path.append('..\\db_access')

from db_access.connect import *
from db_access.api_calls import *

DBconn = DBConnection()
conn = DBconn.conn
cur = conn.cursor()

# cur.execute("DELETE FROM cards")
# cur.execute("DELETE FROM sets")
# conn.commit()

updateSetsTable(conn)
updateCardsTable(conn)