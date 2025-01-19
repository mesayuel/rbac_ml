from flask import Flask, request, jsonify
from models import db, User, Role, Permission
from ml import intent_detector, INTENT_PERMISSION_MAP
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rbac.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return jsonify({'message': 'RBAC App Running'})


@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    username = data.get('username')
    if not username:
        return jsonify({'message': 'Username required'}), 400
    
    user = User(username=username)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': f'User {username} created'}), 201

@app.route('/roles', methods=['POST'])
def add_role():
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({'message': 'Role name required'}), 400
    
    role = Role(name=name)
    db.session.add(role)
    db.session.commit()
    return jsonify({'message': f'Role {name} created'}), 201

@app.route('/permissions', methods=['POST'])
def add_permission():
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({'message': 'Permission name required'}), 400
    
    permission = Permission(name=name)
    db.session.add(permission)
    db.session.commit()
    return jsonify({'message': f'Permission {name} created'}), 201

@app.route('/check_access', methods=['POST'])
def check_access():
    data = request.get_json()
    username = data.get('username')
    user_input = data.get('input_text')
    
    if not username or not user_input:
        return jsonify({'message': 'Username and input_text required'}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    intent = intent_detector.detect(user_input)
    if not intent:
        return jsonify({'message': 'Intent not recognized'}), 400

    required_permissions = INTENT_PERMISSION_MAP.get(intent, [])
    user_permissions = {perm.name for role in user.roles for perm in role.permissions}
    has_access = all(perm in user_permissions for perm in required_permissions)

    return jsonify({
        'username': username,
        'intent': intent,
        'has_access': has_access,
        'user_permissions': list(user_permissions)
    })

if __name__ == '__main__':
    app.run(debug=True)