import unittest
import json
from flask_testing import TestCase
import sys 
import os
# Add backend to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app import create_app
from extensions import db
from models.Employee import Employee
from config import TestingConfig

class TestEmployeeController(TestCase):
    # method required by flask_testing to create and configure the app
    def create_app(self):
        app = create_app(TestingConfig)
        return app
    
    def setUp(self):
        db.create_all()
        
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
class TestRegisterEmployee(TestEmployeeController):
    def setUp(self):
        super().setUp()
        employee = Employee(
            Staff_ID=1,
            Staff_FName='Test',
            Staff_LName='Employee',
            Dept='Test Department',
            Position='Test Position',
            Country='Test Country',
            Email='test@example.com',
            Reporting_Manager=1,  
            Role=1,  # Assuming a valid Role ID
            Password=''
        )
        db.session.add(employee)
        db.session.commit()

    def tearDown(self):
        super().tearDown()

    # happy path
    def test_register_employee(self):
        response = self.client.post('/register', json={
            'employee_id': 1,
            'password': 'testpassword',
            'reconfirm_password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        res_dict = json.loads(response.data)
        
        self.assertEqual('User registered successfully', str(res_dict['message']))
    
    def test_register_employee_missing_fields(self):
        response = self.client.post('/register', json={
            'employee_id': 1,
            'password': 'testpassword'
            # 'reconfirm_password' is missing
        })
        res_dict = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual('All fields are required', str(res_dict['error']))

    def test_register_employee_password_mismatch(self):
        response = self.client.post('/register', json={
            'employee_id': '1',
            'password': 'testpassword',
            'reconfirm_password': 'differentpassword'
        })
        res_dict = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual('Passwords do not match', str(res_dict['error']))

    def test_register_employee_non_existent(self):
        response = self.client.post('/register', json={
            'employee_id': '999',  # Assuming this ID does not exist
            'password': 'testpassword',
            'reconfirm_password': 'testpassword'
        })
        res_dict = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual('No such employee exists', str(res_dict['error']))

    def test_register_employee_already_exists(self): 
        self.client.post('/register', json={
            'employee_id': 1,
            'password': 'testpassword',
            'reconfirm_password': 'testpassword'
        })
        # Attempt to register the same employee again
        response = self.client.post('/register', json={
            'employee_id': '1',
            'password': 'testpassword',
            'reconfirm_password': 'testpassword'
        })
        res_dict = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual('Employee already exists', str(res_dict['error']))
    
    #Happy Path for Login
    def test_login_employee(self):
        self.client.post('/register', json={
            'employee_id': 1,
            'password': 'testpassword',
            'reconfirm_password': 'testpassword'
        })
        response = self.client.post('/login', json={
            'username': '1',
            'password': 'testpassword'
        })
        res_dict = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual('User logged in successfully', str(res_dict['message']))
    
    def test_login_employee_missing_fields(self):
        response = self.client.post('/login', json={
            'username': '1'
            # 'password' is missing
        })
        res_dict = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual('Employee ID and password are required', str(res_dict['error']))
    
    def test_login_employee_not_found(self):
        response = self.client.post('/login', json={
            'username': '999',  # Assuming this ID does not exist
            'password': 'testpassword'
        })
        res_dict = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual('Employee not found', str(res_dict['error']))
    
    def test_login_employee_invalid_password(self): 
        response = self.client.post('/login', json={
            'username': '1',
            'password': 'wrongpassword'
        })
        res_dict = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual('Invalid password', str(res_dict['error']))

    def test_logout_employee(self):
        response = self.client.post('/logout')
        res_dict = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual('User logged out successfully', str(res_dict['message']))
        
if __name__ == '__main__':
    unittest.main()