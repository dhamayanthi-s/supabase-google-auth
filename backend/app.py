from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)  # 👈 Allow CORS for all origins (or restrict to specific origins)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
print(SUPABASE_URL)
print(SERVICE_ROLE_KEY)


@app.route('/api/save-user', methods=['POST'])
def save_user():
    auth_header = request.headers.get('Authorization', '')
    token = auth_header.replace('Bearer ', '')
    print(f'Token: {token}')

    user_check = requests.get(
        f'{SUPABASE_URL}/auth/v1/user',
        headers={
        'Authorization': f'Bearer {token}',
        'apikey': SERVICE_ROLE_KEY  # or your anon/public key if you prefer
    }
    )
    print(user_check.status_code, user_check.text)

    if user_check.status_code != 200:
        return jsonify({'error': 'Unauthorized'}), 401

    user_data = request.get_json()
    email = user_data.get('email')
    name = user_data.get('name')

    # Insert into Supabase 'users' table
    response = requests.post(
        f'{SUPABASE_URL}/rest/v1/users',
        headers={
            'apikey': SERVICE_ROLE_KEY,
            'Authorization': f'Bearer {SERVICE_ROLE_KEY}',
            'Content-Type': 'application/json',
            'Prefer': 'resolution=merge-duplicates'
        },
        json={
            'email': email,
            'name': name
        }
    )
    print(response.status_code, response.text)

    if response.status_code not in [200, 201]:
        return jsonify({'error': 'Failed to save user'}), 500

    return jsonify({'message': 'User saved successfully'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)