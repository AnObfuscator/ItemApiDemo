import requests
from urllib.parse import urljoin

from app.models.item_model import Item

api_path = '/item'
api_path_tpl = api_path + '/{}'


def validate_json_response(response_json, item_id, item_name, item_description):
    """
    Helper method to verify JSON item responses.
    """
    assert response_json['status'] == 'success'

    assert response_json['result']['item_id'] == item_id
    assert response_json['result']['item_name'] == item_name
    assert response_json['result']['item_description'] == item_description


def validate_db_item(db_item, item_id, item_name, item_description):
    """
    Helper method to verify items retrieved from the DB.
    """
    assert db_item.item_id == item_id
    assert db_item.item_name == item_name
    assert db_item.item_description == item_description


class TestGetItemApi:
    """
    Test the GET operations of the Item API
    """

    def test_get_with_empty_db_returns_expected_error(self, service_url, db):
        """
        GET request with no item ID specified

        Setup:
            No items in the DB

        Expected:
            Error response for an invalid request
        """
        response = requests.get(urljoin(service_url, api_path))
        assert response.status_code == 500

    def test_get_by_id_with_empty_db_returns_expected_error(self, service_url, db):
        """
        GET request with item ID specified

        Setup:
            No items in the DB

        Expected:
            Error response for an invalid item
        """
        response = requests.get(urljoin(service_url, api_path_tpl.format('item_42')))
        assert response.status_code == 500

    def test_get_by_id_with_items_returns_expected_item(self, service_url, db):
        """
        GET request with item ID specified

        Setup:
            Specified item is in the DB

        Expected:
            Success response
            Specified item is returned
        """
        db.add(Item(item_id='item_42',
                    item_name="test_item",
                    item_description="test_item_desc"))
        db.commit()

        response = requests.get(urljoin(service_url, api_path_tpl.format('item_42')))
        assert response.status_code == 200

        validate_json_response(response.json(), 'item_42', 'test_item', 'test_item_desc')

    def test_get_by_invalid_id_returns_expected_error(self, service_url, db):
        """
        GET request with item ID specified

        Setup:
            Specified item is not in the DB

        Expected:
            Error response for an invalid item
        """
        db.add(Item(item_id='item_42',
                    item_name="test_item",
                    item_description="test_item_desc"))
        db.commit()

        response = requests.get(urljoin(service_url, api_path_tpl.format('item_24')))
        assert response.status_code == 500


class TestPostItemApi:
    """
    Test the POST operations of the Item API
    """

    def test_post_with_empty_db_creates_expected(self, service_url, db):
        """
        POST request with new item

        Setup:
            None

        Expected:
            Success response
            New item is created
            Created item is returned
        """
        item = {
            'item_id': 'item_24',
            'item_name': 'test_item',
            'item_description': 'test_item_desc'
        }
        response = requests.post(urljoin(service_url, api_path), json=item)
        assert response.status_code == 200
        validate_json_response(response.json(), **item)

        items = db.query(Item).all()
        assert len(items) == 1
        validate_db_item(items[0], **item)

    def test_post_with_missing_desc_creates_expected(self, service_url, db):
        """
        POST request with new item without a description

        Setup:
            None

        Expected:
            Success response
            New item is created
            Created item is returned
        """
        item = {
            'item_id': 'item_24',
            'item_name': 'test_item',
            'item_description': None
        }
        response = requests.post(urljoin(service_url, api_path), json=item)
        assert response.status_code == 200
        validate_json_response(response.json(), **item)

        items = db.query(Item).all()
        assert len(items) == 1
        validate_db_item(items[0], **item)

    def test_post_with_existing_item_creates_expected(self, service_url, db):
        """
        POST request with new item

        Setup:
            Existing item is in the DB

        Expected:
            Success response
            New item is created
            Created item is returned
        """
        db.add(Item(item_id='item_42',
                    item_name='test_item',
                    item_description='test_item_desc'))
        db.commit()

        item = {
            'item_id': 'item_24',
            'item_name': 'test_item',
            'item_description': 'test_item_desc'
        }
        response = requests.post(urljoin(service_url, api_path), json=item)
        assert response.status_code == 200
        validate_json_response(response.json(), **item)

        items = db.query(Item).all()
        assert len(items) == 2
        validate_db_item(items[1], **item)

    def test_post_with_missing_id_returns_expected_error(self, service_url, db):
        """
        POST request with new item without an item ID

        Setup:
            None

        Expected:
            Error response
            No item is created
        """
        item = {
            'item_id': None,
            'item_name': 'test_item',
            'item_description': 'test_item_desc'
        }
        response = requests.post(urljoin(service_url, api_path), json=item)
        assert response.status_code == 500

        items = db.query(Item).all()
        assert len(items) == 0

    def test_post_with_missing_name_returns_expected_error(self, service_url, db):
        """
        POST request with new item without an item name

        Setup:
            None

        Expected:
            Error response
            No item is created
        """
        item = {
            'item_id': 'item_24',
            'item_name': None,
            'item_description': 'test_item_desc'
        }
        response = requests.post(urljoin(service_url, api_path), json=item)
        assert response.status_code == 500

        items = db.query(Item).all()
        assert len(items) == 0

    def test_post_with_no_item_returns_expected_error(self, service_url, db):
        """
        POST request with no new item

        Setup:
            None

        Expected:
            Error response
            No item is created
        """
        response = requests.post(urljoin(service_url, api_path), json=None)
        assert response.status_code == 500

        items = db.query(Item).all()
        assert len(items) == 0

    def test_post_max_id_size_creates_expected(self, service_url, db):
        """
        POST request with new item with ID of maximum size (8 char)

        Setup:
            None

        Expected:
            Success response
            New item is created
            Created item is returned
        """
        item = {
            'item_id': 'x'*8,  # create ID 8 chars long
            'item_name': 'test_item',
            'item_description': 'test_item_desc'
        }
        response = requests.post(urljoin(service_url, api_path), json=item)
        assert response.status_code == 200
        validate_json_response(response.json(), **item)

        items = db.query(Item).all()
        assert len(items) == 1
        validate_db_item(items[0], **item)

    def test_post_over_max_id_size_creates_expected(self, service_url, db):
        """
        POST request with new item with ID greater than max size (> 8 char)

        Setup:
            None

        Expected:
            Error response
            No item is created
        """
        item = {
            'item_id': 'x'*9,  # create ID 9 chars long
            'item_name': 'test_item',
            'item_description': 'test_item_desc'
        }
        response = requests.post(urljoin(service_url, api_path), json=item)
        assert response.status_code == 500

    def test_post_max_name_size_creates_expected(self, service_url, db):
        """
        POST request with new item with name of maximum size (100 char)

        Setup:
            None

        Expected:
            Success response
            New item is created
            Created item is returned
        """
        item = {
            'item_id': 'test_id',
            'item_name': 'x'*100,  # create name 100 chars long
            'item_description': 'test_item_desc'
        }
        response = requests.post(urljoin(service_url, api_path), json=item)
        assert response.status_code == 200
        validate_json_response(response.json(), **item)

        items = db.query(Item).all()
        assert len(items) == 1
        validate_db_item(items[0], **item)

    def test_post_over_max_name_size_creates_expected(self, service_url, db):
        """
        POST request with new item with name greater than max size (> 100 char)

        Setup:
            None

        Expected:
            Error response
            No item is created
        """
        item = {
            'item_id': 'test_id',
            'item_name': 'x'*101,  # create name 101 chars long
            'item_description': 'test_item_desc'
        }
        response = requests.post(urljoin(service_url, api_path), json=item)
        assert response.status_code == 500

    def test_post_max_desc_size_creates_expected(self, service_url, db):
        """
        POST request with new item with description of maximum size (255 char)

        Setup:
            None

        Expected:
            Success response
            New item is created
            Created item is returned
        """
        item = {
            'item_id': 'test_id',
            'item_name': 'test_name',
            'item_description': 'x'*255  # create desc 255 chars long
        }
        response = requests.post(urljoin(service_url, api_path), json=item)
        assert response.status_code == 200
        validate_json_response(response.json(), **item)

        items = db.query(Item).all()
        assert len(items) == 1
        validate_db_item(items[0], **item)

    def test_post_over_max_desc_size_creates_expected(self, service_url, db):
        """
        POST request with new item with description greater than max size (> 255 char)

        Setup:
            None

        Expected:
            Error response
            No item is created
        """
        item = {
            'item_id': 'test_id',
            'item_name': 'test_name',
            'item_description': 'x'*256  # create desc 256 chars long
        }
        response = requests.post(urljoin(service_url, api_path), json=item)
        assert response.status_code == 500


class TestPutItemApi:
    """
    Test the PUT operations of the Item API
    """

    def test_put_update_name_performs_expected_action(self, service_url, db):
        """
        PUT request with new name updates name

        Setup:
            Existing item in the DB

        Expected:
            Success response
            Specified item name is updated
            Updated item is returned
        """
        db.add(Item(item_id='item_42',
                    item_name='test_item',
                    item_description='test_item_desc'))
        db.commit()

        update = {'item_name': 'new_name', 'item_description': 'test_item_desc'}
        response = requests.put(urljoin(service_url, api_path_tpl.format('item_42')), data=update)
        assert response.status_code == 200
        validate_json_response(response.json(), item_id='item_42', **update)

        items = db.query(Item).all()
        assert len(items) == 1
        validate_db_item(items[0], item_id='item_42', **update)

    def test_put_update_to_invalid_name_returns_expected_error(self, service_url, db):
        """
        PUT request with invalid new name returns an error

        Setup:
            Existing item in the DB

        Expected:
            Error response
            Specified item name is not updated
        """
        db.add(Item(item_id='item_42',
                    item_name='test_item',
                    item_description='test_item_desc'))
        db.commit()

        update = {'item_name': 'x'*101, 'item_description': 'test_item_desc'}
        response = requests.put(urljoin(service_url, api_path_tpl.format('item_42')), data=update)
        assert response.status_code == 500

        items = db.query(Item).all()
        assert len(items) == 1
        validate_db_item(items[0], item_id='item_42', item_name='test_item', item_description='test_item_desc')

    def test_put_update_desc_performs_expected_action(self, service_url, db):
        """
        PUT request with new description updates description

        Setup:
            Existing item in the DB

        Expected:
            Success response
            Specified item description is updated
            Updated item is returned
        """
        db.add(Item(item_id='item_42',
                    item_name='test_item',
                    item_description='test_item_desc'))
        db.commit()

        update = {'item_name': 'test_item', 'item_description': 'new_desc'}
        response = requests.put(urljoin(service_url, api_path_tpl.format('item_42')), data=update)
        assert response.status_code == 200
        validate_json_response(response.json(), item_id='item_42', **update)

        items = db.query(Item).all()
        assert len(items) == 1
        validate_db_item(items[0], item_id='item_42', **update)

    def test_put_update_to_invalid_desc_returns_expected_error(self, service_url, db):
        """
        PUT request with invalid new description returns an error

        Setup:
            Existing item in the DB

        Expected:
            Error response
            Specified item description is not updated
        """
        db.add(Item(item_id='item_42',
                    item_name='test_item',
                    item_description='test_item_desc'))
        db.commit()

        update = {'item_name': 'test_item', 'item_description': 'x'*256}
        response = requests.put(urljoin(service_url, api_path_tpl.format('item_42')), data=update)
        assert response.status_code == 500

        items = db.query(Item).all()
        assert len(items) == 1
        validate_db_item(items[0], item_id='item_42', item_name='test_item', item_description='test_item_desc')

    def test_put_update_name_and_desc_performs_expected_action(self, service_url, db):
        """
        PUT request with new name and description updates both

        Setup:
            Existing item in the DB

        Expected:
            Success response
            Specified item fields are updated
            Updated item is returned
        """
        db.add(Item(item_id='item_42',
                    item_name='test_item',
                    item_description='test_item_desc'))
        db.commit()

        update = {'item_name': 'new_name', 'item_description': 'new_desc'}
        response = requests.put(urljoin(service_url, api_path_tpl.format('item_42')), data=update)
        assert response.status_code == 200
        validate_json_response(response.json(), item_id='item_42', **update)

        items = db.query(Item).all()
        assert len(items) == 1
        validate_db_item(items[0], item_id='item_42', **update)

    def test_put_invalid_item_id_returns_expected_error(self, service_url, db):
        """
        PUT request with invalid ID returns an error

        Setup:
            Existing item in the DB

        Expected:
            Error response
            Existing item is not updated
        """
        db.add(Item(item_id='item_42',
                    item_name='test_item',
                    item_description='test_item_desc'))
        db.commit()

        update = {'item_name': 'test_item', 'item_description': 'x' * 256}
        response = requests.put(urljoin(service_url, api_path_tpl.format('invalid_id')), data=update)
        assert response.status_code == 500

        items = db.query(Item).all()
        assert len(items) == 1
        validate_db_item(items[0], item_id='item_42', item_name='test_item', item_description='test_item_desc')

    def test_put_empty_db_returns_expected_error(self, service_url, db):
        """
        PUT request with empty DB returns an error

        Setup:
            No items in the DB

        Expected:
            Error response
        """
        update = {'item_name': 'test_item', 'item_description': 'test_item_desc'}
        response = requests.put(urljoin(service_url, api_path_tpl.format('item_42')), data=update)
        assert response.status_code == 500

        items = db.query(Item).all()
        assert len(items) == 0


class TestDeleteItemApi:
    """
    Test the DELETE operations of the Item API
    """

    def test_delete_removes_expected_item(self, service_url, db):
        """
        DELETE request for existing item

        Setup:
            Existing item is in the DB

        Expected:
            Success response
            Item is removed from DB
        """
        db.add(Item(item_id='item_42',
                    item_name='test_item',
                    item_description='test_item_desc'))
        db.add(Item(item_id='item_24',
                    item_name='test_item',
                    item_description='test_item_desc'))
        db.commit()

        response = requests.delete(urljoin(service_url, api_path_tpl.format('item_42')))
        assert response.status_code == 200
        validate_json_response(response.json(), item_id='item_24', item_name='test_item',
                               item_description='test_item_desc')

        items = db.query(Item).all()
        assert len(items) == 1
        validate_db_item(items[0], item_id='item_24', item_name='test_item', item_description='test_item_desc')

    def test_delete_invalid_item_id_returns_expected_error(self, service_url, db):
        """
        DELETE request for invalid item

        Setup:
            Existing item is in the DB

        Expected:
            Error response
            No item is removed from DB
        """
        db.add(Item(item_id='item_42',
                    item_name='test_item',
                    item_description='test_item_desc'))
        db.commit()

        response = requests.delete(urljoin(service_url, api_path_tpl.format('invalid_item')))
        assert response.status_code == 500

    def test_delete_empty_db_returns_expected_error(self, service_url, db):
        """
        DELETE request for item when the DB is empty

        Setup:
            No item is in the DB

        Expected:
            Error response
        """
        response = requests.delete(urljoin(service_url, api_path_tpl.format('invalid_item')))
        assert response.status_code == 500
