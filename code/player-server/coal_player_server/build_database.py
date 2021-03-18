from .config import db, dbpath, create_app, DefaultConfig
from .models import Player


def build_database():
    if dbpath.exists():
        dbpath.unlink()

    app = create_app(DefaultConfig())
    with app.app.app_context():
        # Create the database
        print("Creating all tables...")
        db.create_all()
