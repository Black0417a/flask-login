from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

# User roles/permissions
ROLE_USER = 0
ROLE_ADMIN = 1
ROLE_MANAGER = 2

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.Integer, default=ROLE_USER)
    
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
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'role_name': self.get_role_name()
        }

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id)) 