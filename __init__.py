import random
import string
import json
from flask import Flask
from flask.ext.mongoengine import MongoEngine

from simplekv.memory import DictStore
from flaskext.kvsession import KVSessionExtension

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = { 'DB' : "my_tubble_log" }
app.config["SECRET_KEY"] = "my_secret"
app.debug = True
app.secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))

store = DictStore();
KVSessionExtension(store, app)

clientId = json.loads( open('oauth_secrets.json', 'r').read())['web']['client_id']

db = MongoEngine(app)

def register_blueprints(app):
    # Prevents circular imports
    from LeagueMgr.views import pages
    app.register_blueprint(pages)

register_blueprints(app)

if __name__ == "__main__" :
    app.run()
