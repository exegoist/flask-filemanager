from flask import Flask
from pony.orm import *

app = Flask(__name__)
app.config["SECRET_KEY"] = "GHhw8sjj29GHts[pkq"

db = Database()
db.bind(provider='sqlite', filename='../database.sqlite', create_db=True)


from app import routes, models
