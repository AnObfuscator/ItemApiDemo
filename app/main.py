import os

from flask import Flask
from flask_restful import Api

from app import db
from app.api.item_api import ItemAPI
from app.config import DB_CONN_STR, API_PORT

# Quick and dirty main script to launch the API
if __name__ == '__main__':
    flask_app = Flask('item_service')
    api = Api(flask_app)
    api.add_resource(ItemAPI, '/item', '/item/<string:item_id>')

    flask_app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONN_STR

    db.init_app(flask_app)

    with flask_app.app_context():
        db.create_all()
        db.session.commit()

    flask_app.run(debug=True, port=API_PORT)
