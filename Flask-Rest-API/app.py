from datetime import timedelta
import MySQLdb
from flask import Flask, request, make_response, jsonify
from flask_jwt_extended import JWTManager
from flask_mysqldb import MySQL
from dicttoxml import dicttoxml
from config import MYSQL_CONFIG

app = Flask(__name__)
app.config.update(MYSQL_CONFIG)
app.config['JWT_SECRET_KEY'] = 'change-this-key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
app.config['JWT_SORT_KEYS'] = False

mysql = MySQL(app)
jwt = JWTManager(app)

VALID_USER = {"username": "admin", "password": "admin123"}

def format_type():
    fmt = request.args.get('format', 'json').lower()
    return fmt if fmt in ('json', 'xml') else 'json'

def format_response(payload, status=200):
    fmt = format_type()
    if fmt == 'xml':
        xml = dicttoxml(payload, custom_root='response', attr_type=False)
        response = make_response(xml, status)
        response.headers['Content-Type'] = 'application/xml'
        return response
    return make_response(jsonify(payload), status)

def success_response(data=None, message=None, status=200):
    body = {}
    if message:
        body['message'] = message
    if data is not None:
        body['data'] = data
    return format_response(body, status)

def error_response(message, status):
    return format_response({'error': message}, status)


@app.route('/')
def home():
    return "Hello, Flask!"


if __name__ == "__main__":
    app.run(debug=True)
