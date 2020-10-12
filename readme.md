
# Item API 

The Item API and tests can be configured and run.

## Configure

A file for pip requirements exists and can be used with this command.

```shell script
pip install -r requirements.txt
```

## Start the app

The application can be configured with two environment variables.

* `API_PORT` defines the port Flask will listen with. It defaults to `5000`.

* `DB_CONN_STR` defines the DB configuration string used by SQLAlchemy. It defaults to the PostgreSQL string I used for testing.

The app can be launched from a shell with the command below:

```shell script
export PYTHONPATH=$PYTHONPATH:app; python app/main.py
```

## Run the tests

The test suite can be configured with two environment variables:

* `SERVICE_URL` defines the fully qualified URL for the API under test. It defaults to `http://127.0.0.1:5000/`.

* `DB_CONN_STR` defines the DB configuration string used by SQLAlchemy. It defaults to the PostgreSQL string I used for testing. This should be the same string used by the application.

The tests can be launched from a shell with the command below:

```shell script
export PYTHONPATH=$PYTHONPATH:app; pytest -s tests/
```

## Database Setup

The database was configured using the following SQL commands.

```postgresql
create user demo with password 'demopass';
create database demodb;
grant all privileges on database demodb to demo;
```

## Test Methodology

The document requested "functional tests", without specifying exactly what is meant by that term. There are multiple competing definitions of "functional test". 

As I was given code and not a specification to test, I interpreted "functional test" the way we used the term on our SDET teams at Rackspace.
 
Thus, these "functional tests" are white box, partial integration tests that are intended to be run against an ephemeral deployment of the application.

## Test Results

Tests were conducted on a Fedora Linux system using Python 3.8 against a PosgreSQL 12 database in a Docker container.

### General Notes
The API does not handle errors well, or use status codes well. Items not found in the DB should result in `404`, deleted items should result in `204`, created items should result in `201`. 

It is standard practice for a `GET` request to the `/item` endpoint to return a list of all items in the DB, paginated if the result set is too large. 

It is standard practice to return no body with a `DELETE` request.

These are not defects per se, but general RESTful design considerations.

### GET Defects
* `Success` is misspelled.

### POST Defects
* `Success` is misspelled.
* Created items are not returned on success

### PUT Defects
* `Success` is misspelled.

### DELETE Defects
* `Success` is misspelled.
* Deleted items are not returned on success
* No error is given for attempting to delete items that do not exist
