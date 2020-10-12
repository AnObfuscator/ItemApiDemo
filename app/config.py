import os


# The port that Flask will listen on.
API_PORT = int(os.environ.get('API_PORT', '5000'))

# The URL to the API.
SERVICE_URL = os.environ.get('SERVICE_URL', 'http://127.0.0.1:5000/')

# The connection string to the database. Obviously I wouldn't put the password in a real config file ;)
DB_CONN_STR = os.environ.get('SQLALCHEMY_DATABASE_URI', 'postgresql+psycopg2://demo:demopass@localhost:5432/demodb')
