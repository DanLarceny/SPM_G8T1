import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from models.Manager import Manager

class TestManagerModel(unittest.TestCase):
    def setUp(self):
        self.manager = Manager(
            Staff_ID=2,
            Staff_FName='John',
            Staff_LName='Doe',
            Dept='IT',
            Position='Developer',
            Country='USA',
            Email='john.doe@example.com',
            Reporting_Manager=3,
            Role=3,
            Password='hashed_password'
        )
        self.mock_application = MagicMock()
        self.mock_application.Application_ID = 100
        

    # happy path for approve_application
    @patch('extensions.db.session.get')
    def test_approve_application(self, mock_get):
        # Mocking WFHApplication
        self.mock_application.Status = 'Pending'
        self.mock_application.Reporting_Manager = self.manager.Staff_ID  # Ensure this matches Reporting_Manager
        # Mock the approve method in WFHApplication
        self.mock_application.approve = MagicMock()
        # Set up the mock to return the application when queried
        mock_get.return_value = self.mock_application

        # Call the method to test
        result = self.manager.approve_application(100)

        # Assertions
        self.assertEqual(result, True)  # Check that it returns True
    
    # negative test case for approve_application
    @patch('extensions.db.Session.get')
    def test_approve_application_no_application(self, mock_get):
        mock_get.return_value = None
        # Call the method to test
        result = self.manager.approve_application(100)

        # Assertions
        self.assertEqual(result, False)
    
    @patch('extensions.db.Session.get')
    def test_approve_application_not_pending(self, mock_get):
        # Mocking WFHApplication
        self.mock_application.Status = 'Approved'
        self.mock_application.Reporting_Manager = self.manager.Staff_ID  # Ensure this matches Reporting_Manager
        # Mock the approve method in WFHApplication
        self.mock_application.approve = MagicMock()
        # Set up the mock to return the application when queried
        mock_get.return_value = self.mock_application

        # Call the method to test
        result = self.manager.approve_application(100)

        # Assertions
        self.assertEqual(result, False)  # Check that it returns False
        mock_get.assert_called_once()  # Ensure that the get method was called 
    
    @patch('extensions.db.Session.get')
    def test_approve_application_not_reporting_manager(self, mock_get):
        # Mocking WFHApplication
        self.mock_application.Status = 'Pending'
        self.mock_application.Reporting_Manager = 4
        
        # Mock the approve method in WFHApplication
        self.mock_application.approve = MagicMock()
        # Set up the mock to return the application when queried
        mock_get.return_value = self.mock_application
        # Call the method to test
        result = self.manager.approve_application(100)

        # Assertions
        self.assertEqual(result, False)  # Check that it returns False
        mock_get.assert_called_once()  # Ensure that the get method was called 
        

    # happy path for reject_application
    @patch('extensions.db.Session.get')
    def test_reject_application(self, mock_get):
        # Mocking WFHApplication
        self.mock_application.Status = 'Pending'
        self.mock_application.Reporting_Manager = self.manager.Staff_ID  # Ensure this matches Reporting_Manager
        
        # Mock the approve method in WFHApplication
        self.mock_application.approve = MagicMock()
        # Set up the mock to return the application when queried
        mock_get.return_value = self.mock_application
        
        
        # Call the method to test
        result = self.manager.reject_application(100)

        # Assertions
        self.assertEqual(result, True)  # Check that it returns True
        mock_get.assert_called_once()  # Ensure that the get method was called 

    
    @patch('extensions.db.Session.get')
    def test_reject_application_no_application(self, mock_get):
        # Mock the get method to return None, simulating no application found
        mock_get.return_value = None
        
        # Call the method to test
        result = self.manager.reject_application(100)

        # Assertions
        self.assertEqual(result, False)  # Should return False since no application exists
        mock_get.assert_called_once()  # Ensure that the get method was called 

    @patch('extensions.db.Session.get')
    def test_reject_application_not_pending(self, mock_get):
        # Mocking WFHApplication
        self.mock_application.Status = 'Approved'  # Status is not "Pending"
        self.mock_application.Reporting_Manager = self.manager.Staff_ID
        
        # Mock the get method to return the application
        mock_get.return_value = self.mock_application
        
        # Call the method to test
        result = self.manager.reject_application(100)

        # Assertions
        self.assertEqual(result, False)  # Should return False since status is not "Pending"
        mock_get.assert_called_once()  # Ensure that the get method was called 

    @patch('extensions.db.Session.get')
    def test_reject_application_not_reporting_manager(self, mock_get):
        # Mocking WFHApplication
        self.mock_application.Status = 'Pending'  # Status is "Pending"
        self.mock_application.Reporting_Manager = 4  # Different Reporting_Manager
        
        # Mock the get method to return the application
        mock_get.return_value = self.mock_application
        
        # Call the method to test
        result = self.manager.reject_application(100)

        # Assertions
        self.assertEqual(result, False)  # Should return False since Reporting_Manager does not match
        mock_get.assert_called_once()  # Ensure that the get method was called 

    @patch('extensions.db.Session.get')
    def test_reject_application_success(self, mock_get):
        # Happy path for reject_application
        self.mock_application.Status = 'Pending'
        self.mock_application.Reporting_Manager = self.manager.Staff_ID
        
        # Mock the reject method in WFHApplication
        self.mock_application.reject = MagicMock()
        
        # Set up the mock to return the application when queried
        mock_get.return_value = self.mock_application
        
        # Call the method to test
        result = self.manager.reject_application(100)

        # Assertions
        self.assertEqual(result, True)  # Check that it returns True
        self.mock_application.reject.assert_called_once()  # Check if the reject method was called
        mock_get.assert_called_once()  # Ensure that the get method was called 
    
    @patch('extensions.db.session.query')
    def test_get_team_schedules(self, mock_query):
        # Mocking WFHSchedule
        mock_schedule = MagicMock()
        mock_schedule.Status = "Approved"

        mock_filter_by = MagicMock()
        mock_filter_by.all.return_value = [mock_schedule]
        mock_query.return_value.filter_by.return_value = mock_filter_by
        
        # Call the method to test
        team_schedules = self.manager.get_team_schedules()
        
        # Assertions
        self.assertEqual(len(team_schedules), 1)  # Check that one schedule is returned
        mock_query.return_value.filter_by.assert_called_once_with(Team_ID=self.manager.Staff_ID)  # Check filter criteria


if __name__ == '__main__':
    unittest.main()
