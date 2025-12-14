from datetime import timedelta
import MySQLdb
from flask import Flask, request, make_response, jsonify
from flask_jwt_extended import JWTManager
from flask_mysqldb import MySQL
from dicttoxml import dicttoxml
from werkzeug.exceptions import HTTPException
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

def validate_game(payload, partial=False):
    if not isinstance(payload, dict):
        return None, "Request body must be a JSON object"
    
    result = {}
    for field in ('game_name', 'game_type'):
        if field in payload:
            value = str(payload[field]).strip()
            if not value:
                return None, f"{field} must be 50 characters or fewer"
            result[field] = value

    if not partial and len(result) != 2:
        missing = [f for f in ('game_name', 'game_type') if f not in result]
        return None, f"Missing fields: {', '.join(missing)}"
    
    if partial and not result:
        return None, "Provide at least one field to update"
    
    return result, None

def get_game_by_id(game_id):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("SELECT game_id, game_name, game_type FROM game WHERE game_id = %s", (game_id,))
        row = cursor.fetchone()
        if row:
            return {'game_id': row['game_id'], 'game_name': row['game_name'], 'game_type': row['game_type']}
        return None
    finally:
        cursor.close()


@app.errorhandler(404)
def handle_404(_):
    return error_response('Resource not found', 404)

@app.errorhandler(Exception)
def handle_exception(err):
    if isinstance(err, HTTPException):
        return err
    if isinstance(err, MySQLdb.Error):
        return error_response('Database error occurred', 500)
    return error_response('Internal server error', 500)


@app.route('/')
def home():
    return "Hello, Flask!"


if __name__ == "__main__":
    app.run(debug=True)
