from app import create_app, db
from app.models import User, ROLE_USER, ROLE_ADMIN, ROLE_MANAGER

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 
        'User': User,
        'ROLE_USER': ROLE_USER,
        'ROLE_ADMIN': ROLE_ADMIN,
        'ROLE_MANAGER': ROLE_MANAGER
    }

if __name__ == '__main__':
    app.run(debug=True) 