from datetime import timedelta
import MySQLdb
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_mysqldb import MySQL
from config import MYSQL_CONFIG

class APIError(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

app = Flask(__name__)
app.config.update(MYSQL_CONFIG)
app.config['JWT_SECRET_KEY'] = 'change-this-key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
app.config['JWT_SORT_KEYS'] = False

mysql = MySQL(app)
jwt = JWTManager(app)

VALID_USER = {"username": "admin", "password": "admin123"}
SEARCHABLE_FIELDS = {
    'game_id': 'game_id',
    'game_name': 'game_name',
    'game_type': 'game_type'
}

@app.route('/')
def home():
    return "Hello, Flask!"


if __name__ == "__main__":
    app.run(debug=True)
