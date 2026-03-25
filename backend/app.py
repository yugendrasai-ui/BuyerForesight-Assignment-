import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from database import db, ma
from models import User, user_schema, users_schema
from sqlalchemy import or_

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app) 
basedir = os.path.abspath(os.path.dirname(__file__))

@app.route('/')
def index():
    return app.send_static_file('index.html')

# Database Configuration
# Render uses 'postgresql://', but some legacy tools use 'postgres://'
db_url = os.environ.get('DATABASE_URL')
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url or 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB and Marshmallow
db.init_app(app)
ma.init_app(app)

# Create Database tables
with app.app_context():
    db.create_all()

# --- Endpoints ---

@app.route('/users', methods=['POST'])
def add_user():
    name = request.json.get('name')
    email = request.json.get('email')
    role = request.json.get('role', 'user')

    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    new_user = User(name=name, email=email, role=role)
    
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Email already exists or database error"}), 400

    return user_schema.jsonify(new_user), 201

@app.route('/users', methods=['GET'])
def get_users():
    search = request.args.get('search')
    sort = request.args.get('sort', 'id')
    order = request.args.get('order', 'asc')

    query = User.query

    if search:
        query = query.filter(or_(User.name.icontains(search), User.email.icontains(search)))

    if order == 'desc':
        query = query.order_by(db.desc(getattr(User, sort, User.id)))
    else:
        query = query.order_by(getattr(User, sort, User.id))

    all_users = query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return user_schema.jsonify(user)

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    name = request.json.get('name')
    email = request.json.get('email')
    role = request.json.get('role')

    if name: user.name = name
    if email: user.email = email
    if role: user.role = role

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Database error"}), 400

    return user_schema.jsonify(user)

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)

if __name__ == '__main__':
    app.run(debug=True)
