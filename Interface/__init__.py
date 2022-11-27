import sys

from flask import Flask, render_template, blueprints
from Interface.Website import create_app
from markupsafe import escape
from .connect import *

user = DBConnection('asdf', 'asdf') # user in 'users' table; NOT the Database user, which will be the same for everyone
if(user.cursor.rowcount != 0):
    print('Connected')

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

# This was a test to get card info

#original_stdout = sys.stdout # Save a reference to the original standard output
# with open('pkmn_w_ability.txt', 'w') as f:
#     sys.stdout = f # Change the standard output to the file we created.
#     card = Card.find('bw1-6')1
#     #getNewSet('xy1')
#     print(card)
#     sys.stdout = original_stdout # Reset the standard output to its original value
#     exit

# ancient traits use special chars like α, which require utf-8 (as opposed to default ascii)
# with open('pkmn_w_ancientTrait.txt', 'w', encoding='utf-8') as f:
#     sys.stdout = f # Change the standard output to the file we created.
#     card = Card.find('xy5-104')
#     #getNewSet('xy1')
#     print(card)
#     sys.stdout = original_stdout # Reset the standard output to its original value
#     exit