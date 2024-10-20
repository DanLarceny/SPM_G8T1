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
    
    @patch('extensions.db.session.commit')
    def test_approve(self, mock_commit):
        self.application.approve()
        self.assertEqual(self.application.Status, "Approved")

    @patch('extensions.db.session.commit')
    def test_reject(self, mock_commit):
        self.application.reject()
        self.assertEqual(self.application.Status, "Rejected")
        mock_commit.assert_called_once()  # Ensure commit was called
    
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
    
    @patch('models.WFH_Application.db.session')
    def test_create_application_success(self, mock_session):
        """Test successful creation of an application."""
        # Mock valid inputs
        application = WFHApplication.createApplication(
            staff_id=1,
            start_date='2024-10-21',
            end_date='2024-10-23',
            time_slot='morning',
            selected_days=['Monday', 'Wednesday'],
            email='test@example.com',
            reason='Personal',
            type='WFH',
            reporting_manager='Manager',
            file='encoded_file_string'
        )

        # Assert session was used correctly
        mock_session.add.assert_called_once_with(application)
        mock_session.commit.assert_called_once()

        # Assert application fields
        self.assertEqual(application.Staff_ID, 1)
        self.assertEqual(application.Status, 'Pending')
        self.assertEqual(application.Time_Slot, 'morning')
        self.assertEqual(application.Email, 'test@example.com')
        self.assertEqual(application.Days, 'Monday,Wednesday')

    @patch('models.WFH_Application.db.session')
    def test_create_application_empty_days(self, mock_session):
        """Test creation with no selected days."""
        application = WFHApplication.createApplication(
            staff_id=2,
            start_date='2024-11-01',
            end_date='2024-11-02',
            time_slot='evening',
            selected_days=None,
            email='test2@example.com',
            reason='Work',
            type='WFH',
            reporting_manager='Another Manager',
            file='file_string'
        )

        # Assert the Days field is None
        self.assertIsNone(application.Days)

    @patch('models.WFH_Application.WFHApplication.query')
    def test_search_for_available_dates(self, mock_query):
        # Mock existing applications
        mock_query.filter.return_value.all.return_value = [
            WFHApplication(
                Application_ID=1,
                Staff_ID=100,
                Start_Date=datetime(2024, 11, 1),
                End_Date=datetime(2024, 11, 3),
                Status="Approved",
                Time_Slot="AM",
                Type="AdHoc",
                Email="employee@example.com",
                Reporting_Manager=200,
                Days="Mon,Tue"
            )
        ]

        available_dates = WFHApplication.searchForAvailableDates(staff_id=100, start_date='2024-11-01', end_date='2024-11-07')
        expected_dates = ['2024-11-04', '2024-11-05', '2024-11-06', '2024-11-07']
        self.assertEqual(available_dates, expected_dates)

    @patch('models.WFH_Application.WFHApplication.query')
    def test_search_for_available_dates_no_conflicts(self, mock_query):
        # Mock no existing applications
        mock_query.filter.return_value.all.return_value = []

        available_dates = WFHApplication.searchForAvailableDates(staff_id=100, start_date='2024-11-01', end_date='2024-11-07')
        expected_dates = ['2024-11-01', '2024-11-02', '2024-11-03', '2024-11-04', '2024-11-05', '2024-11-06', '2024-11-07']
        self.assertEqual(available_dates, expected_dates)

    @patch('models.WFH_Application.WFHApplication.query')
    def test_search_for_available_dates_exception(self, mock_query):
        # Simulate a database error
        mock_query.filter.side_effect = Exception("Database error")
        
        with self.assertRaises(Exception) as context:
            WFHApplication.searchForAvailableDates(
                staff_id=100, start_date='2024-11-01', end_date='2024-11-03'
            )
        
        self.assertEqual(str(context.exception), "Database error")
    
    @patch('models.WFH_Application.WFHApplication.query')
    def test_display_available_dates(self, mock_query):
        start_date = '2024-11-01'
        end_date = '2024-11-05'
        expected_dates = ['2024-11-01', '2024-11-02', '2024-11-03', '2024-11-04', '2024-11-05']
        available_dates = WFHApplication.displayAvailableDates(start_date, end_date)
        self.assertEqual(available_dates, expected_dates)
    
    @patch('models.WFH_Application.WFHApplication.query')
    def test_get_all_arrangement_valid(self, mock_query):
        # Mock the query to return a list of applications
        mock_query.filter.return_value.all.return_value = [
            WFHApplication(
                Application_ID=1,
                Staff_ID=100,
                Start_Date=datetime(2024, 11, 1),
                End_Date=datetime(2024, 11, 3),
                Status="Approved"
            ),
            WFHApplication(
                Application_ID=2,
                Staff_ID=100,
                Start_Date=datetime(2024, 11, 4),
                End_Date=datetime(2024, 11, 5),
                Status="Pending"
            )
        ]
        
        applications = WFHApplication.getAllArrangement(
            staff_id=100, start_date='2024-11-01', end_date='2024-11-07'
        )
        
        self.assertEqual(len(applications), 2)
        self.assertEqual(applications[0].Application_ID, 1)
        self.assertEqual(applications[1].Application_ID, 2)

    @patch('models.WFH_Application.WFHApplication.query')
    def test_get_all_arrangement_empty(self, mock_query):
        # Mock the query to return an empty list
        mock_query.filter.return_value.all.return_value = []
        
        applications = WFHApplication.getAllArrangement(
            staff_id=100, start_date='2024-11-01', end_date='2024-11-07'
        )
        
        self.assertEqual(len(applications), 0)

    @patch('models.WFH_Application.WFHApplication.query')
    def test_get_all_arrangement_exception(self, mock_query):
        # Simulate a database error
        mock_query.filter.side_effect = Exception("Database error")
        
        with self.assertRaises(Exception) as context:
            WFHApplication.getAllArrangement(
                staff_id=100, start_date='2024-11-01', end_date='2024-11-07'
            )
        
        self.assertEqual(str(context.exception), "Database error")

        
            
if __name__ == '__main__':
    unittest.main()