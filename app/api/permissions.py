from flask import jsonify, request, g
from app import db
from app.api import bp
from app.models.user import Permission, User
from app.api.auth import token_auth, current_user
from app.api.errors import bad_request, error_response
from datetime import datetime

@bp.route('/permissions', methods=['GET'])
@token_auth.login_required
def get_permissions():
    if not current_user().has_admin_access():
        return error_response(403, "Admin access required")
    
    permissions = Permission.query.all()
    return jsonify([p.to_dict() for p in permissions])

@bp.route('/permissions/<int:id>', methods=['GET'])
@token_auth.login_required
def get_permission(id):
    if not current_user().has_admin_access():
        return error_response(403, "Admin access required")
    
    permission = Permission.query.get_or_404(id)
    return jsonify(permission.to_dict())

@bp.route('/permissions', methods=['POST'])
@token_auth.login_required
def create_permission():
    if not current_user().has_admin_access():
        return error_response(403, "Admin access required")
    
    data = request.get_json() or {}
    if 'name' not in data or 'description' not in data:
        return bad_request('Must include name and description fields')
    
    if Permission.query.filter_by(name=data['name']).first():
        return bad_request(f"Permission with name '{data['name']}' already exists")
    
    permission = Permission(name=data['name'], description=data['description'])
    db.session.add(permission)
    db.session.commit()
    
    return jsonify(permission.to_dict()), 201

@bp.route('/permissions/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_permission(id):
    if not current_user().has_admin_access():
        return error_response(403, "Admin access required")
    
    permission = Permission.query.get_or_404(id)
    data = request.get_json() or {}
    
    if 'name' in data and data['name'] != permission.name and \
            Permission.query.filter_by(name=data['name']).first():
        return bad_request(f"Permission with name '{data['name']}' already exists")
    
    if 'name' in data:
        permission.name = data['name']
    if 'description' in data:
        permission.description = data['description']
    
    db.session.commit()
    return jsonify(permission.to_dict())

@bp.route('/permissions/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_permission(id):
    if not current_user().has_admin_access():
        return error_response(403, "Admin access required")
    
    permission = Permission.query.get_or_404(id)
    db.session.delete(permission)
    db.session.commit()
    
    return '', 204

@bp.route('/users/<int:id>/permissions', methods=['GET'])
@token_auth.login_required
def get_user_permissions(id):
    user_making_request = current_user()
    if not user_making_request.has_admin_access() and user_making_request.id != id:
        return error_response(403, "Not authorized to view this user's permissions")
    
    user = User.query.get_or_404(id)
    return jsonify([p.to_dict() for p in user.permissions])

@bp.route('/users/<int:id>/permissions', methods=['PUT'])
@token_auth.login_required
def update_user_permissions(id):
    if not current_user().has_admin_access():
        return error_response(403, "Admin access required")
    
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    
    if 'permission_ids' not in data:
        return bad_request('Must include permission_ids field')
    
    # Clear existing permissions
    user.permissions = []
    
    # Add new permissions
    for perm_id in data['permission_ids']:
        permission = Permission.query.get(perm_id)
        if permission:
            user.add_permission(permission)
    
    db.session.commit()
    return jsonify([p.to_dict() for p in user.permissions]) 