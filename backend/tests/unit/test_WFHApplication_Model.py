import unittest
import sys
import os

from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

# Add backend to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from extensions import db
from app import create_app


from models.WFH_Application import WFHApplication

class Test_WFHApplicationModel(unittest.TestCase): 
    def setUp(self): 
        self.app = create_app()  # Use the imported Flask app instance
        self.app_context = self.app.app_context()
        self.app_context.push()  # Push the app context to make it active
    
        self.application = WFHApplication(
            Application_ID = 1,
            Staff_ID = 100,
            Start_Date = datetime(2024, 11, 1),
            End_Date = datetime(2024, 11, 7),
            Status = "pending",
            Time_Slot="AM",
            Type="AdHoc",
            Email="employee@example.com",
            Reporting_Manager=200,
            Days="Mon,Tue,Wed"
        )
    
    def tearDown(self): 
        pass

    def test_create_application(self):
        self.assertIsInstance(self.application, WFHApplication)
        self.assertEqual(self.application.Application_ID, 1)
        self.assertEqual(self.application.Staff_ID, 100)
        self.assertEqual(self.application.Status, "pending")
    
    def test_approve(self):
        self.application.approve()
        self.assertEqual(self.application.Status, "Approved")

    def test_reject(self):
        self.application.reject()
        self.assertEqual(self.application.Status, "Rejected")
    
    
    def test_approve_rejected_application(self):
        self.application.reject()
        with self.assertRaises(ValueError):
            self.application.approve()
    
    def test_approve_case_insensitive(self):
        self.application.Status = "PENDING"
        self.application.approve()
        self.assertEqual(self.application.Status, "Approved")

        self.application.Status = "pending"
        self.application.approve()
        self.assertEqual(self.application.Status, "Approved")
    
    def test_reject_case_insensitive(self):
        self.application.Status = "PENDING"
        self.application.reject()
        self.assertEqual(self.application.Status, "Rejected")

        self.application.Status = "pending"
        self.application.reject()
        self.assertEqual(self.application.Status, "Rejected")
    
    def test_to_dict(self):
        expected_dict = {
            'Application_ID': 1,
            'Staff_ID': 100,
            'Start_Date': self.application.Start_Date.strftime('%Y-%m-%d'),
            'End_Date': self.application.End_Date.strftime('%Y-%m-%d'),
            'Status': "pending",
            'Time_Slot': "AM",
            'Type': "AdHoc",
            'Email': "employee@example.com",
            'Reporting_Manager': 200
        }
        self.assertEqual(self.application.to_dict(), expected_dict)
    
    def test_to_dict_with_boundary_dates(self):
        # Test with minimum date
        self.application.Start_Date = datetime.min
        self.application.End_Date = datetime.min
        expected_dict = {
            'Application_ID': 1,
            'Staff_ID': 100,
            'Start_Date': self.application.Start_Date.strftime('%Y-%m-%d'),
            'End_Date': self.application.End_Date.strftime('%Y-%m-%d'),
            'Status': "pending",
            'Time_Slot': "AM",
            'Type': "AdHoc",
            'Email': "employee@example.com",
            'Reporting_Manager': 200
        }
        self.assertEqual(self.application.to_dict(), expected_dict)

        # Test with maximum date
        self.application.Start_Date = datetime.max
        self.application.End_Date = datetime.max
        expected_dict = {
            'Application_ID': 1,
            'Staff_ID': 100,
            'Start_Date': self.application.Start_Date.strftime('%Y-%m-%d'),
            'End_Date': self.application.End_Date.strftime('%Y-%m-%d'),
            'Status': "pending",
            'Time_Slot': "AM",
            'Type': "AdHoc",
            'Email': "employee@example.com",
            'Reporting_Manager': 200
        }

    def test_to_dict_with_missing_attributes(self):
        # Simulate missing attributes by creating a new application without some fields
        incomplete_application = WFHApplication(
            Application_ID=2,
            Staff_ID=101,
            Start_Date=datetime(2024, 11, 1),
            End_Date=datetime(2024, 11, 7),
            Status=None,  # Missing status
            Time_Slot=None,  # Missing time slot
            Type=None,  # Missing type
            Email=None,  # Missing email
            Reporting_Manager=None  # Missing reporting manager
        )
        expected_dict = {
            'Application_ID': 2,
            'Staff_ID': 101,
            'Start_Date': incomplete_application.Start_Date.strftime('%Y-%m-%d'),
            'End_Date': incomplete_application.End_Date.strftime('%Y-%m-%d'),
            'Status': None,
            'Time_Slot': None,
            'Type': None,
            'Email': None,
            'Reporting_Manager': None
        }
        self.assertEqual(incomplete_application.to_dict(), expected_dict)
    
    def test_get_selected_days_with_valid_days(self):
        application = WFHApplication(
            Application_ID=1,
            Staff_ID=100,
            Start_Date=datetime(2024, 11, 1),
            End_Date=datetime(2024, 11, 7),
            Status="pending",
            Time_Slot="AM",
            Type="AdHoc",
            Email="employee@example.com",
            Reporting_Manager=200,
            Days="Mon,Tue,Wed"
        )
        expected_days = ["Mon", "Tue", "Wed"]
        self.assertEqual(application.get_selected_days(), expected_days)
    
    def test_get_selected_days_with_empty_string(self):
        application = WFHApplication(
            Application_ID=2,
            Staff_ID=101,
            Start_Date=datetime(2024, 11, 1),
            End_Date=datetime(2024, 11, 7),
            Status="pending",
            Time_Slot="AM",
            Type="AdHoc",
            Email="employee@example.com",
            Reporting_Manager=200,
            Days=""
        )
        expected_days = []
        self.assertEqual(application.get_selected_days(), expected_days)
    
    def test_get_selected_days_with_none(self):
        application = WFHApplication(
            Application_ID=3,
            Staff_ID=102,
            Start_Date=datetime(2024, 11, 1),
            End_Date=datetime(2024, 11, 7),
            Status="pending",
            Time_Slot="AM",
            Type="AdHoc",
            Email="employee@example.com",
            Reporting_Manager=200,
            Days=None
        )
        expected_days = []
        self.assertEqual(application.get_selected_days(), expected_days)
    
    @patch('models.WFH_Application.WFHApplication.query')
    def test_get_arrangement_valid(self, mock_query):
        # Mock the return value of the query
        mock_query.filter.return_value.first.return_value = self.application
        
        application = WFHApplication.getArrangement(staff_id=100, application_id=1)
        self.assertIsNotNone(application)
        self.assertEqual(application.Application_ID, 1)
        self.assertEqual(application.Staff_ID, 100)

    @patch('models.WFH_Application.WFHApplication.query')
    def test_get_arrangement_invalid_application_id(self, mock_query):
        # Mock the return value of the query to return None
        mock_query.filter.return_value.first.return_value = None
        
        application = WFHApplication.getArrangement(staff_id=100, application_id=999)  # Non-existent application ID
        self.assertIsNone(application)
    
    @patch('models.WFH_Application.WFHApplication.query')
    def test_get_arrangement_non_existent_staff(self, mock_query):
        # Mock the return value of the query to return None
        mock_query.filter.return_value.first.return_value = None
        
        application = WFHApplication.getArrangement(staff_id=999, application_id=1)  # Non-existent staff ID
        self.assertIsNone(application)

    @patch('models.WFH_Application.WFHApplication.query')
    def test_get_arrangement_database_error(self, mock_query):
        # Simulate a database error by raising an exception when filter is called
        mock_query.filter.side_effect = Exception("Database error")
        
        with self.assertRaises(Exception) as context:
            WFHApplication.getArrangement(staff_id=100, application_id=1)
        
        self.assertEqual(str(context.exception), "Database error")
        
            
if __name__ == '__main__':
    unittest.main()