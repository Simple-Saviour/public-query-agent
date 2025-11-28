import json
import os

def load_mock_users():
    """
    Loads users from data/mock_users.json using an absolute path.
    """
    # 1. Get the directory where THIS file (helpers.py) lives
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Go up one level to the project root (citizen-query-assistant/)
    root_dir = os.path.dirname(current_dir)
    
    # 3. Construct the full path to the json file
    file_path = os.path.join(root_dir, "data", "mock_users.json")
    
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        # Print error to terminal so you can see if it fails
        print(f"❌ ERROR: Could not find mock_users.json at: {file_path}")
        return {"users": []}

def check_login(username, password):
    """
    Verifies credentials against the loaded JSON data.
    """
    data = load_mock_users()
    
    # Clean input (remove accidental spaces)
    clean_user = username.strip()
    clean_pwd = password.strip()
    
    for user in data.get("users", []):
        # Check matching credentials
        if user["username"] == clean_user and user["password"] == clean_pwd:
            return user["role"]
            
    return None