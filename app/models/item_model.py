# app/models/item_model.py
from app import db


class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    item_id = db.Column(db.String(8), nullable=False, index=True, unique=True)
    item_name = db.Column(db.String(100), nullable=False, index=True)
    item_description = db.Column(db.String(255), nullable=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def __init__(self, **kwargs):
        self.item_id = kwargs.get('item_id')
        self.item_name = kwargs.get('item_name')
        self.item_description = kwargs.get('item_description')

    def __repr__(self):
        return "<Item {0} {1} {2}>".format(self.item_id, self.item_name, self.item_description)
