import unittest
from app import app, db
from models import User, Role, Permission

class TestApp(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        
        # Create application context and database tables
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Clean up after each test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home(self):
        """Test home endpoint"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'RBAC App Running')

    def test_add_user(self):
        """Test adding a user"""
        # Test successful user creation
        response = self.client.post('/users', json={'username': 'Alice'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('User Alice created', response.json['message'])

        # Test missing username
        response = self.client.post('/users', json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Username required')

    def test_add_role(self):
        """Test adding a role"""
        # Test successful role creation
        response = self.client.post('/roles', json={'name': 'Editor'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Role Editor created', response.json['message'])

        # Test missing role name
        response = self.client.post('/roles', json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Role name required')

    def test_add_permission(self):
        """Test adding a permission"""
        # Test successful permission creation
        response = self.client.post('/permissions', json={'name': 'edit_document'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Permission edit_document created', response.json['message'])

        # Test missing permission name
        response = self.client.post('/permissions', json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Permission name required')

    def test_check_access_with_permissions(self):
        """Test checking access for a user with appropriate permissions"""
        # Create user
        self.client.post('/users', json={'username': 'Alice'})
        user = User.query.filter_by(username='Alice').first()

        # Create role
        self.client.post('/roles', json={'name': 'Editor'})
        role = Role.query.filter_by(name='Editor').first()

        # Create permission
        self.client.post('/permissions', json={'name': 'edit_document'})
        permission = Permission.query.filter_by(name='edit_document').first()

        # Assign permission to role and role to user
        role.permissions.append(permission)
        user.roles.append(role)
        db.session.commit()

        # Test access check
        response = self.client.post('/check_access', 
            json={
                'username': 'Alice',
                'input_text': 'Can I edit this document?'
            })
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['has_access'])
        self.assertEqual(response.json['intent'], 'edit_document')

    def test_check_access_without_permissions(self):
        """Test checking access for a user without appropriate permissions"""
        # Create user without any roles/permissions
        self.client.post('/users', json={'username': 'Bob'})

        # Test access check
        response = self.client.post('/check_access', 
            json={
                'username': 'Bob',
                'input_text': 'Can I edit this document?'
            })
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json['has_access'])

    def test_check_access_invalid_requests(self):
        """Test check_access endpoint with invalid requests"""
        # Test missing username
        response = self.client.post('/check_access', 
            json={'input_text': 'Can I edit this document?'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Username and input_text required')

        # Test missing input_text
        response = self.client.post('/check_access', 
            json={'username': 'Alice'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Username and input_text required')

        # Test non-existent user
        response = self.client.post('/check_access', 
            json={
                'username': 'NonExistentUser',
                'input_text': 'Can I edit this document?'
            })
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['message'], 'User not found')

    def test_unrecognized_intent(self):
        """Test handling of unrecognized intents"""
        # Create user
        self.client.post('/users', json={'username': 'Alice'})

        # Test with unrecognized intent
        response = self.client.post('/check_access', 
            json={
                'username': 'Alice',
                'input_text': 'Can I fly this document to the moon?'
            })
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Intent not recognized')

if __name__ == '__main__':
    unittest.main()