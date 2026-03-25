# User Management REST API

A simple User Management API built with Flask and SQLite.

## Requirements
- Python 3.8+
- Flask
- Flask-SQLAlchemy
- Flask-Marshmallow
- marshmallow-sqlalchemy

## Installation
1. Clone the repository (or navigate to the folder).
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the API
Run the Flask application:
```bash
python app.py
```
The API will be available at `http://127.0.0.1:5000`.

## API Endpoints

### 1. List Users
- **GET** `/users`
- **Query Parameters**:
  - `search`: Search by name or email (e.g., `?search=alice`)
  - `sort`: Field to sort by (default: `id`)
  - `order`: Sort order (`asc` or `desc`, default: `asc`)

### 2. Get User Details
- **GET** `/users/:id`

### 3. Create User
- **POST** `/users`
- **Body** (JSON):
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "role": "admin"
  }
  ```

### 4. Update User
- **PUT** `/users/:id`
- **Body** (JSON):
  ```json
  {
    "name": "John Updated"
  }
  ```

### 5. Delete User
- **DELETE** `/users/:id`

## Testing
To run the automated tests:
```bash
python test_api.py
```
*Note: Make sure the server is stopped before running the test script as it manages the server process internally (or edit it to connect to a running server).*
