from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login
from datetime import datetime

# User role constants
ROLE_USER = 0
ROLE_ADMIN = 1
ROLE_MANAGER = 2

# User-Permission association table
user_permissions = db.Table('user_permissions',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'), primary_key=True)
)

class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Permission {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.Integer, default=ROLE_USER)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Additional permission flags for simplified access control
    can_view_reports = db.Column(db.Boolean, default=False)
    can_edit_content = db.Column(db.Boolean, default=False)
    can_manage_users = db.Column(db.Boolean, default=False)
    
    # Relationship with permissions
    permissions = db.relationship('Permission', secondary=user_permissions,
                                  lazy='subquery', backref=db.backref('users', lazy=True))
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_role_name(self):
        roles = {
            ROLE_USER: 'User',
            ROLE_ADMIN: 'Admin',
            ROLE_MANAGER: 'Manager'
        }
        return roles.get(self.role, 'Unknown')
    
    def has_admin_access(self):
        return self.role == ROLE_ADMIN
    
    def has_manager_access(self):
        return self.role == ROLE_MANAGER
    
    def has_permission(self, permission_name):
        return any(p.name == permission_name for p in self.permissions)
    
    def add_permission(self, permission):
        if permission not in self.permissions:
            self.permissions.append(permission)
    
    def remove_permission(self, permission):
        if permission in self.permissions:
            self.permissions.remove(permission)
    
    # For Flask-Login - prevent deactivated users from logging in
    def is_authenticated(self):
        return super().is_authenticated and self.is_active
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'role_name': self.get_role_name(),
            'is_active': self.is_active,
            'permissions': [p.to_dict() for p in self.permissions],
            'can_view_reports': self.can_view_reports,
            'can_edit_content': self.can_edit_content, 
            'can_manage_users': self.can_manage_users,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id)) 