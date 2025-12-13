from flask import Flask
from flask_mysqldb import MySQL
from config import MYSQL_CONFIG

app = Flask(__name__)
app.config.update(MYSQL_CONFIG)

mysql = MySQL(app)


@app.route('/')
def home():
    return "Hello, Flask!"


if __name__ == "__main__":
    app.run(debug=True)
