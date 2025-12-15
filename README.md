# Flask REST API - Esports Game Management System

A secure RESTful API for managing esports games, built with Flask and MySQL, featuring JWT authentication and support for both JSON and XML response formats.

---

## 📋 Project Overview

This Flask-based REST API provides a comprehensive system for managing esports game data. The application implements CRUD (Create, Read, Update, Delete) operations for game records with secure JWT token-based authentication. It connects to a MySQL database (`esportsdb`) that contains information about esports games, teams, and players.

The API is designed to be flexible and developer-friendly, supporting both JSON and XML response formats based on client preferences. It includes robust error handling, input validation, and follows RESTful design principles.

---

## 🛠️ Technologies Used

- **Python 3.x** - Core programming language
- **Flask 3.1.0** - Lightweight web framework for building the REST API
- **Flask-JWT-Extended 4.7.1** - JWT authentication implementation
- **Flask-MySQLdb 2.0.0** - MySQL database integration
- **MySQL 8.0** - Relational database management system
- **mysqlclient 2.2.7** - Python MySQL database connector
- **dicttoxml 1.7.16** - XML response format conversion
- **Werkzeug 3.1.3** - WSGI web application library
- **Jinja2 3.1.6** - Template engine for Flask
- **PyJWT 2.10.1** - JSON Web Token implementation

---

## 📁 Project Structure

```
Flask-Rest-API/
├── app.py                  # Main application file with API endpoints
├── config.py               # Database configuration settings
├── esportsdb.sql          # Database schema and sample data
├── requirements.txt        # Python package dependencies
└── __pycache__/           # Python bytecode cache
```

### File Descriptions

- **app.py** - The main application file containing:
  - Flask app initialization and configuration
  - JWT authentication setup
  - API route definitions for CRUD operations
  - Helper functions for validation and response formatting
  - Error handlers for graceful error management

- **config.py** - Configuration file containing:
  - MySQL database connection parameters
  - Database host, user, password, and database name settings

- **esportsdb.sql** - SQL dump file containing:
  - Database schema definitions
  - Table structures for `game`
  - Sample data for testing and development

- **requirements.txt** - Lists all Python package dependencies required to run the application

---

## 🗄️ Database Schema

The application uses the **esportsdb** MySQL database with the following tables:

### 1. **game** Table
Stores information about esports games.

| Column     | Type        | Description                    |
|------------|-------------|--------------------------------|
| game_id    | INT (PK)    | Unique game identifier         |
| game_name  | VARCHAR(50) | Name of the esports game       |
| game_type  | VARCHAR(45) | Game genre/type (MOBA, FPS, etc.) |

**Purpose**: Primary table for game management operations. All CRUD operations in the API target this table.

**Sample Data**: Mobile Legends (MOBA), Valorant (FPS), PUBG Mobile (Battle Royale), etc.


---

## 🚀 Installation and Setup Instructions

### Prerequisites

- Python 3.8 or higher
- MySQL Server 8.0 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Project

```bash
cd flask-rest/Flask-Rest-API/Flask-Rest-API
```

### Step 2: Create and Activate Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Setup MySQL Database

1. Start your MySQL server
2. Create the database and import the schema:

```bash
mysql -u root -p
```

```sql
CREATE DATABASE esportsdb;
USE esportsdb;
SOURCE esportsdb.sql;
```

Or use MySQL Workbench to import the `esportsdb.sql` file.

### Step 5: Configure Database Connection

Edit `config.py` with your MySQL credentials:

```python
MYSQL_CONFIG = {
    "MYSQL_HOST": "localhost",
    "MYSQL_USER": "your_username",
    "MYSQL_PASSWORD": "your_password",
    "MYSQL_DB": "esportsdb",
    "MYSQL_PORT": 3306,
    "MYSQL_CURSORCLASS": "DictCursor",
}
```

### Step 6: Run the Application

```bash
python app.py
```

The API will be available at `http://127.0.0.1:5000/`

---

## ✨ Key Features

### 1. **JWT Authentication**
- Secure token-based authentication
- 30-minute token expiration
- Protected endpoints requiring valid tokens

### 2. **CRUD Operations**
- **Create**: Add new games to the database
- **Read**: Retrieve all games or specific game by ID
- **Update**: Modify existing game information
- **Delete**: Remove games from the database

### 3. **Flexible Response Formats**
- JSON (default)
- XML (by adding `?format=xml` to requests)

### 4. **Advanced Filtering**
- Search games by name
- Filter games by type
- Support for partial matches

### 5. **Input Validation**
- Comprehensive request payload validation
- Field presence and format checks
- Meaningful error messages

### 6. **Error Handling**
- Custom error handlers for 404 and 500 errors
- Database error management
- Graceful exception handling

### 7. **RESTful Design**
- Standard HTTP methods (GET, POST, PUT, DELETE)
- Consistent endpoint structure
- Appropriate HTTP status codes

---

## 🔌 API Endpoints

### Authentication

| Method | Endpoint | Description        | Auth Required |
|--------|----------|--------------------|---------------|
| POST   | /login   | Login and get JWT  | No            |

### Game Management

| Method | Endpoint           | Description              | Auth Required |
|--------|--------------------|--------------------------|---------------|
| GET    | /games             | Get all games (with filters) | Yes       |
| GET    | /games/:id         | Get specific game        | Yes           |
| POST   | /games             | Create new game          | Yes           |
| PUT    | /games/:id         | Update game              | Yes           |
| DELETE | /games/:id         | Delete game              | Yes           |

### Example Login Request

```bash
curl -X POST http://127.0.0.1:5000/login -H "Content-Type: application/json" -d "{\"username\":\"admin\",\"password\":\"admin123\"}"
```

**Response:**
```json
{
  "data": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  },
  "message": "Login successful"
}
```

### Example Create Game Request

```bash
curl -X POST http://127.0.0.1:5000/games -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_REAL_TOKEN" -d "{\"game_name\":\"Rocket League\",\"game_type\":\"Sports\"}"
```

### XML Response Example

Add `?format=xml` to any endpoint:

```bash
curl http://127.0.0.1:5000/games?format=xml -H "Authorization: Bearer YOUR_REAL_TOKEN"
```

---

## 👤 Author Information

**Name:** Samir D. Araah

**Project:** Flask REST API - Esports Game Management System

**Year:** 2025

---

## 📝 Notes

- Default login credentials: `username: admin`, `password: admin123`
- Change the JWT secret key in production (`app.config['JWT_SECRET_KEY']`)
- Token expires after 30 minutes
- The API runs in debug mode by default (disable in production)

---
