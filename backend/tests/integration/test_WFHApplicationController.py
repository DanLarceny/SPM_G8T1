import unittest
import json
import sys
import os
# Add backend to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from flask_testing import TestCase
from unittest.mock import patch, MagicMock
from models.Employee import Employee
from models.WFH_Application import WFHApplication
from config import TestingConfig
from app import create_app
from extensions import db


class TestWFHApplicationController(TestCase):
    # method required by flask_testing to create and configure the app
    def create_app(self):
        app = create_app(TestingConfig)
        return app
    
    def setUp(self):
        db.create_all()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestWFHApplicationControllerTests(TestWFHApplicationController):
    def setUp(self):
        super().setUp()
        # Mock the Employee instance for testing
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
            Password='testpassword'
        )
        db.session.add(employee)
        db.session.commit()

    # Happy path: create WFH application
    @patch('models.WFH_Application.WFHApplication')  # Mock the WFHApplication model
    def test_apply_wfh(self, MockWFHApplication):
        mock_instance = MockWFHApplication.return_value
        mock_instance.Application_ID = 1  # Mock the Application ID

        response = self.client.post('/createApplication', json={
            'employee_id': 1,
            'start_date': '2024-12-18',
            'end_date': '2024-12-25',
            'time_slot': 'PM',
            'selected_days': ['Monday', 'Wednesday'],
            'email': 'test@example.com',
            'reason': 'Personal reasons',
            'type': 'Recurring',
            "file": 'base64encodedfile'
            
        })
        res_dict = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue('Application_ID' in res_dict['data'])

    # Test missing required fields
    @patch('models.WFH_Application.WFHApplication')  # Mock the WFHApplication model
    def test_apply_wfh_missing_fields(self, MockWFHApplication):
        response = self.client.post('/createApplication', json={
            'employee_id': 1,
            'start_date': '2024-10-18',
            'end_date': '2024-10-25',
            'time_slot': 'PM',
            # Missing email and reason
            'type': 'Recurring',
            "file": 'base64encodedfile'
            
        })
        res_dict = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual('Missing required fields', str(res_dict['error']))

    # Test invalid date format
    @patch('models.WFH_Application.WFHApplication')  # Mock the WFHApplication model
    def test_apply_wfh_invalid_date(self, MockWFHApplication):
        response = self.client.post('/createApplication', json={
            'employee_id': 1,
            'start_date': 'invalid_date',  # Invalid date format
            'end_date': '2024-10-25',
            'time_slot': 'PM',
            'email': 'test@example.com',
            'reason': 'Personal reasons',
            'type': 'Recurring',
            "file": 'base64encodedfile'
            
        })
        res_dict = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue('Invalid date format' in str(res_dict['error']))

    # Test application for non-existent employee
    @patch('models.WFH_Application.WFHApplication')  # Mock the WFHApplication model
    def test_apply_wfh_non_existent_employee(self, MockWFHApplication):
        response = self.client.post('/createApplication', json={
            'employee_id': 999,  # Assuming this ID does not exist
            'start_date': '2024-10-18',
            'end_date': '2024-10-25',
            'time_slot': 'PM',
            'email': 'test@example.com',
            'reason': 'Personal reasons',
            'type': 'Recurring',
            "file": 'base64encodedfile'
        })
        res_dict = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual('Employee not found', str(res_dict['error']))

    # Test applying for past dates
    @patch('models.WFH_Application.WFHApplication')  # Mock the WFHApplication model
    def test_apply_wfh_past_dates(self, MockWFHApplication):
        response = self.client.post('/createApplication', json={
            'employee_id': 1,
            'start_date': '2024-01-01',  # Past date
            'end_date': '2024-01-10',
            'time_slot': 'PM',
            'email': 'test@example.com',
            'reason': 'Personal reasons',
            'type': 'Recurring',
            "file": 'base64encodedfile'
        })
        res_dict = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual('Cannot apply for past time blocks.', str(res_dict['error']))

    # Test invalid date range
    @patch('models.WFH_Application.WFHApplication')  # Mock the WFHApplication model
    def test_apply_wfh_invalid_date_range(self, MockWFHApplication):
        response = self.client.post('/createApplication', json={
            'employee_id': 1,
            'start_date': '2024-12-25',
            'end_date': '2024-12-18',  # End date before start date
            'time_slot': 'PM',
            'email': 'test@example.com',
            'reason': 'Personal reasons',
            'type': 'Recurring',
            "file": 'base64encodedfile'
        })
        res_dict = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual('Start Date cannot be after End Date.', str(res_dict['error']))

if __name__ == '__main__':
    unittest.main()

