from flask import request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app.models import User
from app.auth import bp
import jwt
import datetime
from flask import current_app


@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 400

    # Create new user
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])

    # Set role if provided
    if 'role' in data and data['role'] in [0, 1, 2]:
        user.role = data['role']

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


@bp.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return jsonify(current_user.to_dict()), 200

    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user is None or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid username or password'}), 401

    login_user(user)

    # Generate JWT token
    token = jwt.encode({
        'sub': user.id,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},
        current_app.config['JWT_SECRET_KEY'])

    return jsonify({
        'token': token,
        'user': user.to_dict()
    }), 200


@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200


@bp.route('/user', methods=['GET'])
@login_required
def get_user():
    return jsonify(current_user.to_dict()), 200
