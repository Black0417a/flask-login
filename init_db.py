from app import create_app, db
from app.models import User, ROLE_USER, ROLE_ADMIN, ROLE_MANAGER

app = create_app()

with app.app_context():
    # Create database tables
    db.create_all()
    
    # Check if admin user exists
    if User.query.filter_by(username='admin').first() is None:
        admin = User(username='admin', email='admin@example.com', role=ROLE_ADMIN)
        admin.set_password('admin123')
        db.session.add(admin)
    
    # Check if manager user exists
    if User.query.filter_by(username='manager').first() is None:
        manager = User(username='manager', email='manager@example.com', role=ROLE_MANAGER)
        manager.set_password('manager123')
        db.session.add(manager)
    
    # Check if regular user exists
    if User.query.filter_by(username='user').first() is None:
        user = User(username='user', email='user@example.com', role=ROLE_USER)
        user.set_password('user123')
        db.session.add(user)
    
    db.session.commit()
    
    print("Database initialized with default users.")
    print("Admin credentials: admin / admin123")
    print("Manager credentials: manager / manager123")
    print("User credentials: user / user123") 