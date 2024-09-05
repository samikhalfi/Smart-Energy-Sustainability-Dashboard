import yaml

USER_FILE = 'config/users.yaml'

def load_users():
    try:
        with open(USER_FILE, 'r') as file:
            return yaml.safe_load(file) or {}
    except FileNotFoundError:
        return {}

def save_users(users_data):
    with open(USER_FILE, 'w') as file:
        yaml.safe_dump(users_data, file)

def get_hashed_password(username):
    users_data = load_users()
    user = users_data.get('users', {}).get(username)
    if user:
        return user.get('password').encode()  # Return hashed password as bytes
    return None

def store_user_credentials(username, email, hashed_password):
    users_data = load_users()
    if 'users' not in users_data:
        users_data['users'] = {}
    users_data['users'][username] = {
        'email': email,
        'password': hashed_password.decode()  # Store as string
    }
    save_users(users_data)
