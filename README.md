# Flask Login Backend

A Flask backend for the login module with role-based permissions.

## Features

- User authentication with Flask-Login
- JWT token generation
- Role-based permissions (User, Manager, Admin)
- API endpoints for user management
- SQLAlchemy ORM for database operations

## Setup

1. Activate the virtual environment:

```bash
# On Windows
venv\Scripts\activate
```

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Initialize the database:

```bash
python init_db.py
```

4. Run the application:

```bash
python run.py
```

The application will run on http://localhost:5000

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get JWT token
- `POST /auth/logout` - Logout
- `GET /auth/user` - Get current user info

### User Management
- `GET /api/users` - Get all users (Admin only)
- `GET /api/users/<id>` - Get user by ID (Own user or Admin)
- `PUT /api/users/<id>/role` - Update user role (Admin only)
- `GET /api/permissions` - Get current user permissions

## Default Users

The system is initialized with three default users:

1. Admin user:
   - Username: admin
   - Password: admin123
   - Role: Admin

2. Manager user:
   - Username: manager
   - Password: manager123
   - Role: Manager

3. Regular user:
   - Username: user
   - Password: user123
   - Role: User 