from .config import db, dbpath
from .models import Room


def build_database():
    if dbpath.exists():
        dbpath.unlink()

    # Create the database
    print("Creating all tables...")
    db.create_all()
