from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_bootstrap import Bootstrap5

app = Flask(__name__)

# this must be set before we create the database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
# create the data base
db = SQLAlchemy(app)
app.secret_key = "tO$&!|0wkamvVia0?n$NqIRVWOG"

# Bootstrap-Flask requires this line
bootstrap = Bootstrap5(app)
# Flask-WTF requires this line
csrf = CSRFProtect(app)

from app import routes
