from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory storage for users
users = []

def validate_user_data(data):
    """Validate user data"""
    if not isinstance(data, dict):
        return False, "User data must be a dictionary"
    
    # Check required fields
    if 'username' not in data or not data['username']:
        return False, "Username is required"
    
    if 'email' not in data or not data['email']:
        return False, "Email is required"
    
    # Basic email validation
    if '@' not in data['email']:
        return False, "Invalid email format"
    
    return True, ""

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/users', methods=['POST'])
def create_user():
    user = request.get_json()
    
    # Validate user data
    is_valid, error_message = validate_user_data(user)
    if not is_valid:
        return jsonify({'error': error_message}), 400
    
    users.append(user)
    return jsonify(user), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    if user_id < len(users):
        return jsonify(users[user_id])
    return jsonify({'error': 'User not found'}), 404

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if user_id < len(users):
        user_data = request.get_json()
        
        # Validate user data
        is_valid, error_message = validate_user_data(user_data)
        if not is_valid:
            return jsonify({'error': error_message}), 400
        
        users[user_id] = user_data
        return jsonify(users[user_id])
    return jsonify({'error': 'User not found'}), 404

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id < len(users):
        deleted = users.pop(user_id)
        return jsonify(deleted)
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)