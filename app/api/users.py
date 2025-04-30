from flask import jsonify, request
from app import db
from app.models import User, ROLE_USER, ROLE_ADMIN, ROLE_MANAGER
from app.api import bp
from flask_login import login_required, current_user

@bp.route('/users', methods=['GET'])
@login_required
def get_users():
    # Only admin can get all users
    if not current_user.has_admin_access():
        return jsonify({'message': 'Unauthorized access'}), 403
    
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

@bp.route('/users/<int:id>', methods=['GET'])
@login_required
def get_user(id):
    # Users can only get their own info unless they are admin
    if current_user.id != id and not current_user.has_admin_access():
        return jsonify({'message': 'Unauthorized access'}), 403
    
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict()), 200

@bp.route('/users/<int:id>/role', methods=['PUT'])
@login_required
def update_user_role(id):
    # Only admin can update roles
    if not current_user.has_admin_access():
        return jsonify({'message': 'Unauthorized access'}), 403
    
    user = User.query.get_or_404(id)
    data = request.get_json()
    
    if 'role' not in data or data['role'] not in [ROLE_USER, ROLE_ADMIN, ROLE_MANAGER]:
        return jsonify({'message': 'Invalid role'}), 400
    
    user.role = data['role']
    db.session.commit()
    
    return jsonify(user.to_dict()), 200

@bp.route('/users/<int:id>', methods=['PUT'])
@login_required
def update_user(id):
    # Only admin can update other users
    if current_user.id != id and not current_user.has_admin_access():
        return jsonify({'message': 'Unauthorized access'}), 403
    
    user = User.query.get_or_404(id)
    data = request.get_json()
    
    # Update basic info
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    
    # Only admin can update these fields
    if current_user.has_admin_access():
        if 'role' in data and data['role'] in [ROLE_USER, ROLE_ADMIN, ROLE_MANAGER]:
            user.role = data['role']
        
        if 'is_active' in data:
            user.is_active = bool(data['is_active'])
        
        # Update user permissions
        if 'permissions' in data:
            permissions = data['permissions']
            
            if 'can_view_reports' in permissions:
                user.can_view_reports = bool(permissions['can_view_reports'])
            
            if 'can_edit_content' in permissions:
                user.can_edit_content = bool(permissions['can_edit_content'])
            
            if 'can_manage_users' in permissions:
                user.can_manage_users = bool(permissions['can_manage_users'])
    
    db.session.commit()
    return jsonify(user.to_dict()), 200

@bp.route('/users/<int:id>/status', methods=['PUT'])
@login_required
def toggle_user_status(id):
    # Only admin can toggle user status
    if not current_user.has_admin_access():
        return jsonify({'message': 'Unauthorized access'}), 403
    
    user = User.query.get_or_404(id)
    data = request.get_json()
    
    if 'is_active' in data:
        user.is_active = bool(data['is_active'])
        db.session.commit()
    
    return jsonify(user.to_dict()), 200

@bp.route('/user-roles', methods=['GET'])
@login_required
def get_user_roles():
    return jsonify({
        'roles': {
            'user': ROLE_USER,
            'admin': ROLE_ADMIN,
            'manager': ROLE_MANAGER
        },
        'user_role': current_user.role,
        'is_admin': current_user.has_admin_access(),
        'is_manager': current_user.has_manager_access()
    }), 200 