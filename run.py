#!flask/bin/python
from app import app

import webbrowser

#app.run(debug = True)

from os import environ
if 'WINGDB_ACTIVE' in environ:
    app.debug = False
    webbrowser.open("http://127.0.0.1:5000")
app.run()