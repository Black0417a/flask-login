from app import create_app, db
from app.models import User, Permission, ROLE_USER, ROLE_ADMIN, ROLE_MANAGER

app = create_app()

with app.app_context():
    # Create database tables
    db.create_all()
    
    # Create default permissions
    default_permissions = [
        {'name': 'view_users', 'description': 'Can view user list'},
        {'name': 'create_user', 'description': 'Can create new users'},
        {'name': 'edit_user', 'description': 'Can edit user information'},
        {'name': 'delete_user', 'description': 'Can delete users'},
        {'name': 'assign_permissions', 'description': 'Can assign permissions to users'},
        {'name': 'view_reports', 'description': 'Can view reports'},
        {'name': 'manage_system', 'description': 'Can manage system settings'}
    ]
    
    permission_objects = {}
    for perm in default_permissions:
        existing = Permission.query.filter_by(name=perm['name']).first()
        if not existing:
            new_perm = Permission(name=perm['name'], description=perm['description'])
            db.session.add(new_perm)
            permission_objects[perm['name']] = new_perm
        else:
            permission_objects[perm['name']] = existing
    
    db.session.commit()
    
    # Check if admin user exists
    admin = User.query.filter_by(username='admin').first()
    if admin is None:
        admin = User(username='admin', email='admin@example.com', role=ROLE_ADMIN)
        admin.set_password('admin123')
        db.session.add(admin)
    
    # Assign all permissions to admin
    for perm in permission_objects.values():
        admin.add_permission(perm)
    
    # Check if manager user exists
    manager = User.query.filter_by(username='manager').first()
    if manager is None:
        manager = User(username='manager', email='manager@example.com', role=ROLE_MANAGER)
        manager.set_password('manager123')
        db.session.add(manager)
    
    # Assign some permissions to manager
    manager_perms = ['view_users', 'view_reports', 'edit_user']
    for perm_name in manager_perms:
        if perm_name in permission_objects:
            manager.add_permission(permission_objects[perm_name])
    
    # Check if regular user exists
    user = User.query.filter_by(username='user').first()
    if user is None:
        user = User(username='user', email='user@example.com', role=ROLE_USER)
        user.set_password('user123')
        db.session.add(user)
    
    # Assign limited permissions to user
    user_perms = ['view_reports']
    for perm_name in user_perms:
        if perm_name in permission_objects:
            user.add_permission(permission_objects[perm_name])
    
    db.session.commit()
    
    print("Database initialized with default users and permissions.")
    print("Admin credentials: admin / admin123")
    print("Manager credentials: manager / manager123")
    print("User credentials: user / user123") 