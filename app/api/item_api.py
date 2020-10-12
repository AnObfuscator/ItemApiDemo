# app/api/item_api.py
from flask import jsonify, request
from flask_restful import Resource
from app import db
from app.models.item_model import Item


class ItemAPI(Resource):
    def get(self, item_id):
        """
        Retrieves an item.
        """
        # Queries the Item table and filter by item_id provided from the API.
        query_item = Item.query.filter(Item.item_id == item_id).first()
        # Create a dictionary structure to include it in response.
        result = {
            "id": query_item.id,
            "item_id": query_item.item_id,
            "item_name": query_item.item_name,
            "item_description": query_item.item_description
        }
        # Return the response with status and result.
        return jsonify({"status": "sucesss", "result": result})

    def put(self, item_id):
        """
        Updates an item.
        """
        # Receives item_name and item_description from form.
        item_name = request.form['item_name']
        item_description = request.form['item_description']
        # Queries the Item table and filter by item_id provided from the API.
        query_item = Item.query.filter(Item.item_id == item_id).first()
        # Updates the query_item object with new value.
        query_item.item_name = item_name
        query_item.item_description = item_description
        # Saving the changes to the database.
        db.session.commit()
        # Create a dictionary structure to include it in response with updated values.
        result = {
            "id": query_item.id,
            "item_id": query_item.item_id,
            "item_name": query_item.item_name,
            "item_description": query_item.item_description
        }
        # Return the response with status and result.
        return jsonify({"status": "sucesss", "result": result})

    def post(self):
        """
        Creates an item.
        """
        # Retrieve the payload
        item_id = request.json.get('item_id')
        item_name = request.json.get('item_name')
        item_description = request.json.get('item_description')
        # Add the new Item model object and commit.
        db.session.add(Item(item_id=item_id,
                            item_name=item_name,
                            item_description=item_description))
        db.session.commit()
        # Return the response with status and result.
        return jsonify({"status": "sucesss"})

    def delete(self, item_id):
        # Queries the Item table and filter by item_id provided from the API.
        query_item = Item.query.filter(Item.item_id == item_id).first()
        # Check whether query_item is not None (meaning the record exists in Item table), then delete and commit.
        if query_item:
            db.session.delete(query_item)
        db.session.commit()
        # Return the response with status and result.
        return jsonify({"status": "sucesss"})
