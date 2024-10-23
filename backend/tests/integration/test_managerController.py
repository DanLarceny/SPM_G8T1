import unittest
import json
from flask_testing import TestCase
import sys 
import os
from datetime import datetime
# Add backend to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app import create_app
from unittest.mock import patch
from extensions import db
from models.Employee import Employee
from models.Manager import Manager
from models.WFH_Application import WFHApplication
from models.Role import Role
from models.WFH_Schedule import WFHSchedule
from config import TestingConfig


class TestManagerController(TestCase):
    # method required by flask_testing to create and configure the app
    def create_app(self):
        app = create_app(TestingConfig)
        return app

    def setUp(self):
        db.create_all()
        if not Role.query.get(3):
            manager_role = Role(Role=3, Role_Name='Manager')
            db.session.add(manager_role)

        if not Role.query.get(2):
            staff_role = Role(Role=2, Role_Name='Staff')
            db.session.add(staff_role)

        if not Role.query.get(1):
            hr_role = Role(Role=1, Role_Name='HR/Director')
            db.session.add(hr_role)

        db.session.commit()

        # Add manager
        manager = Employee(
            Staff_ID=12345,
            Staff_FName='testFname',
            Staff_LName='testLname',
            Dept='testDept',
            Position='Manager',
            Country='testCountry',
            Email='manager@example.com',
            Reporting_Manager=12345,  
            Role=3,
            Password='testpassword'
        )
        db.session.add(manager)
        db.session.commit()

        # employee who requires manager to approve requests
        employee = Employee(
            Staff_ID=12346,
            Staff_FName='Jane',
            Staff_LName='Smith',
            Dept='Engineering',
            Position='Engineer',
            Country='USA',
            Email='jane.smith@example.com',
            Reporting_Manager=12345, # Manager's ID
            Role=2,
            Password='password123'
        )
        db.session.add(employee)
        db.session.commit()

        wfh_application = WFHApplication(
            Application_ID=1,
            Staff_ID=12346,  # Employee's ID
            Start_Date=datetime(2023, 10, 1),
            End_Date=datetime(2023, 10, 10),
            Status='Pending',
            Time_Slot='Day',
            Type='AdHoc',
            Email='jane.smith@example.com',
            Reporting_Manager=12345,  # Manager's ID
            Reason='Medical leave',
            Encoded_File=None
        )
        db.session.add(wfh_application)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
    # happy path
    def test_view_pending_wfh_requests(self):
        response = self.client.get('/viewPendingWFHRequests/12345')  
        res_dict = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(res_dict) > 0)
        self.assertEqual(res_dict[0]['application_id'], 1)
        self.assertEqual(res_dict[0]['staff_id'], 12346)
        self.assertEqual(res_dict[0]['status'], 'Pending')
        self.assertEqual(res_dict[0]['email'], 'jane.smith@example.com')

    def test_no_pending_wfh_requests(self):
        WFHApplication.query.delete()
        db.session.commit()

        response = self.client.get('/viewPendingWFHRequests/12345') 
        res_dict = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res_dict['message'], 'No pending requests found')
    
    def test_multiple_pending_requests(self):
        another_wfh_application = WFHApplication(
            Application_ID=2,
            Staff_ID=12346,
            Start_Date=datetime(2023, 10, 15),
            End_Date=datetime(2023, 10, 20),
            Status='Pending',
            Time_Slot='Day',
            Type='AdHoc',
            Email='jane.smith@example.com',
            Reporting_Manager=12345,
            Reason='Personal leave',
            Encoded_File=None
        )
        db.session.add(another_wfh_application)
        db.session.commit()

        response = self.client.get('/viewPendingWFHRequests/12345')
        res_dict = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(res_dict), 2)

    # edge cases

    def test_view_pending_wfh_requests_invalid_manager(self):
        response = self.client.get('/viewPendingWFHRequests/999') 
        res_dict = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(res_dict['error'], 'Manager not found')

    def test_view_pending_wfh_requests_invalid_manager_id(self):
        response = self.client.get('/viewPendingWFHRequests/abc') 
        res_dict = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(res_dict['error'], 'Manager not found')
    
    def test_post_request(self):
        response = self.client.post('/viewPendingWFHRequests/12345') 
        self.assertEqual(response.status_code, 405)  
    

    @patch('models.WFH_Application.WFHApplication.query.get')
    @patch('models.Employee.Employee.query.filter_by')
    def test_approve_wfh_request_success(self, mock_employee_query, mock_wfh_query):
        # Mock the employee and WFH application
        mock_employee = Employee(Staff_ID=1)
        mock_wfh_request = WFHApplication(Application_ID=1, Status='Pending', Reporting_Manager=1)
        
        mock_employee_query.return_value.first.return_value = mock_employee
        mock_wfh_query.return_value = mock_wfh_request

        response = self.client.post('/approveWFHRequest/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Request approved', response.get_json()['message'])
        
    @patch('models.WFH_Application.WFHApplication.query.get')
    @patch('models.Employee.Employee.query.filter_by')
    def test_approve_wfh_request_not_found(self, mock_employee_query, mock_wfh_query):
        # Mock the employee and WFH application
        mock_employee_query.return_value.first.return_value = None
        mock_wfh_query.return_value = None

        response = self.client.post('/approveWFHRequest/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Request not found', response.get_json()['error'])

    @patch('models.WFH_Application.WFHApplication.query.get')
    @patch('models.Employee.Employee.query.filter_by')
    def test_reject_wfh_request_success(self, mock_employee_query, mock_wfh_query):
        # Mock the employee and WFH application
        mock_employee = Employee(Staff_ID=1)
        mock_wfh_request = WFHApplication(Application_ID=1, Status='Pending', Reporting_Manager=1)
        
        mock_employee_query.return_value.first.return_value = mock_employee
        mock_wfh_query.return_value = mock_wfh_request

        response = self.client.post('/rejectWFHRequest/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Request rejected', response.get_json()['message'])

    @patch('models.WFH_Application.WFHApplication.query.get')
    @patch('models.Employee.Employee.query.filter_by')
    def test_reject_wfh_request_not_found(self, mock_employee_query, mock_wfh_query):
        # Mock the employee and WFH application
        mock_employee_query.return_value.first.return_value = None
        mock_wfh_query.return_value = None

        response = self.client.post('/rejectWFHRequest/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Request not found', response.get_json()['error'])

    @patch('models.WFH_Application.WFHApplication.query.get')
    @patch('models.Employee.Employee.query.filter_by')
    def test_view_wfh_request_details_success(self, mock_employee_query, mock_wfh_query):
        # Mock the WFH application and employee
        mock_wfh_request = WFHApplication(Application_ID=1, Staff_ID=1, Start_Date=datetime(2024, 11, 1, 9, 0, 0), End_Date=datetime(2024, 11, 5, 17, 0, 0))
        mock_employee = Employee(Staff_ID=1, Staff_FName="John", Staff_LName="Doe")
        
        mock_wfh_query.return_value = mock_wfh_request
        mock_employee_query.return_value = mock_employee

        response = self.client.get('/viewWFHRequestDetails/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('requester_name', response.get_json())
        self.assertIn('request_date_time', response.get_json())
        self.assertIn('requested_wfh_dates', response.get_json())

    @patch('models.WFH_Application.WFHApplication.query.get')
    def test_view_wfh_request_details_request_not_found(self, mock_wfh_query):
        mock_wfh_query.return_value = None

        response = self.client.get('/viewWFHRequestDetails/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Request not found', response.get_json()['error'])

if __name__ == '__main__':
    unittest.main()