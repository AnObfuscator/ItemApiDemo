"""
Basic utils to help tests interacting with the database
"""
from app.models.item_model import Item

tables = [Item]


def clear_db(session):
    """
    Utility function to remove all items in the test database.
    """
    for table in tables:
        session.query(table).delete()
        session.commit()
