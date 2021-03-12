import os
from pathlib import Path

import connexion
from connexion.resolver import RestyResolver
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

dbpath = Path(__file__).parent / "coal.db"

# Create the Connexion application instance
options = {"swagger_ui": False}
connex_app = connexion.App(
    __name__,
    specification_dir="./openapi",
    options=options,
    resolver=RestyResolver("coal_game_server.controllers"),
)

# Get the underlying Flask app instance
app = connex_app.app

# Configure the SQLAlchemy part of the app instance
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////" + str(dbpath)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)
