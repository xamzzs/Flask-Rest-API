from datetime import timedelta
import MySQLdb
from flask import Flask, request, make_response, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
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
    return success_response(message='API is running')

@app.route('/login', methods=['POST'])
def login():
    creds = request.get_json(silent=True) or {}
    username = str(creds.get('username', '')).strip()
    password = str(creds.get('password', '')).strip()

    if username != VALID_USER['username'] or password != VALID_USER['password']:
        return error_response('Invalid username or password', 401)

    token = create_access_token(identity=username)
    return success_response({'access_token': token}, 'Login successful')

@app.route('/games', methods=['GET'])
@jwt_required()
def list_games():
    name_filter = request.args.get('game_name', '').strip()
    type_filter = request.args.get('game_type', '').strip()

    cursor = mysql.connection.cursor()
    try:
        query = "SELECT game_id, game_name, game_type FROM game"
        conditions = []
        params = []

        if name_filter:
            conditions.append("game_name LIKE %s")
            params.append(f"%{name_filter}%")
        if type_filter:
            conditions.append("game_type LIKE %s")
            params.append(f"%{type_filter}%")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += " ORDER BY game_id"

        cursor.execute(query, params)
        games = [{'game_id': r['game_id'], 'game_name': r['game_name'], 'game_type': r['game_type']}
                 for r in cursor.fetchall()]
    finally:
        cursor.close()

    msg = "Games found" if games else "No games matched your search"
    return success_response(games, msg)

@app.route('/games/<int:game_id>', methods=['GET'])
@jwt_required()
def get_game(game_id):
    game = get_game_by_id(game_id)
    if not game:
        return error_response('Game not found', 404)
    return success_response(game)

@app.route('/games', methods=['POST'])
@jwt_required()
def create_game():
    data = request.get_json(silent=True)
    clean, err = validate_game(data)
    if err:
        return error_response(err, 400)

    cursor = mysql.connection.cursor()
    try:
        cursor.execute("INSERT INTO game (game_name, game_type) VALUES (%s, %s)",
                       (clean['game_name'], clean['game_type']))
        mysql.connection.commit()
        new_id = cursor.lastrowid
    finally:
        cursor.close()

    new_game = get_game_by_id(new_id)
    return success_response(new_game, 'Game created', 201)

@app.route('/games/<int:game_id>', methods=['PUT'])
@jwt_required()
def update_game(game_id):
    data = request.get_json(silent=True)
    clean, err = validate_game(data, partial=True)
    if err:
        return error_response(err, 400)

    cursor = mysql.connection.cursor()
    try:
        set_clause = ', '.join(f"{k} = %s" for k in clean)
        params = list(clean.values()) + [game_id]
        cursor.execute(f"UPDATE game SET {set_clause} WHERE game_id = %s", params)
        mysql.connection.commit()
        if cursor.rowcount == 0:
            return error_response('Game not found', 404)
    finally:
        cursor.close()

    updated_game = get_game_by_id(game_id)
    return success_response(updated_game, 'Game updated')

@app.route('/games/<int:game_id>', methods=['DELETE'])
@jwt_required()
def delete_game(game_id):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("DELETE FROM game WHERE game_id = %s", (game_id,))
        mysql.connection.commit()
        if cursor.rowcount == 0:
            return error_response('Game not found', 404)
    finally:
        cursor.close()

    return success_response(message='Game deleted')

if __name__ == "__main__":
    app.run(debug=True)
