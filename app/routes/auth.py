from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app import db
from app.models import User
import json

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'user')

    if User.query.filter_by(email=email).first():
        return jsonify({'msg': 'User already exists'}), 409

    hashed_pw = generate_password_hash(password)
    user = User(email=email, password=hashed_pw, role=role)
    db.session.add(user)
    db.session.commit()
    return jsonify({'msg': 'User registered successfully'})

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        token = create_access_token(identity=json.dumps({'id': user.id, 'role': user.role}))
        return jsonify({'access_token': token})
    return jsonify({'msg': 'Invalid credentials'}), 401
