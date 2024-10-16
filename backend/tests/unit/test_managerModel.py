# import unittest
# import sys
# import os
# # Add backend to the path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# from unittest.mock import MagicMock, patch
# from models.Manager import Manager
# from models.WFH_Application import WFHApplication
# from models.WFH_Schedule import WFHSchedule
# from datetime import datetime

# class TestManagerModel(unittest.TestCase):
#     def setUp(self):
#         self.manager = Manager(
#             Staff_ID=2,
#             Staff_FName='John',
#             Staff_LName='Doe',
#             Dept='IT',
#             Position='Developer',
#             Country='USA',
#             Email='john.doe@example.com',
#             Reporting_Manager=3,
#             Role=3,
#             Password='hashed_password'
#         )


#     @patch('extensions.db.session.commit')
#     @patch('extensions.db.Model.query')
#     def test_approve_application(self, mock_query, mock_commit):
#         application = WFHApplication(
#             Application_ID = 100,
#             Staff_ID = 1,
#             Start_Date = datetime(2024, 10, 12, 6, 56, 4, 387232),
#             End_Date = datetime(2025, 10, 12, 6, 56, 4, 387232),
#             Status = 'Pending',
#             Time_Slot = 'Day',
#             Type = 'Recurring',
#             Email = 'john.doe@example.com',
#             Reporting_Manager = 2
#         )

#         # Set up the mock to return the application when queried
#         mock_query.get.return_value = application

#         # Create a Manager instance with the corresponding Staff_ID
#         manager = Manager()
#         manager.Staff_ID = 2  # Ensure this matches Reporting_Manager

#         # Call the method to test
#         result = manager.approve_application(100)

#         # Assertions
#         self.assertEqual(result, True)  # Check that it returns True
#         self.assertEqual(application.Status, 'Approved')  # Check if the status was updated

#     @patch('extensions.db.session.commit')
#     @patch('extensions.db.Model.query')
#     def test_reject_application(self, mock_query, mock_commit):
#         application = WFHApplication(
#             Application_ID = 100,
#             Staff_ID = 1,
#             Start_Date = datetime(2024, 10, 12, 6, 56, 4, 387232),
#             End_Date = datetime(2025, 10, 12, 6, 56, 4, 387232),
#             Status = 'Pending',
#             Time_Slot = 'Day',
#             Type = 'Recurring',
#             Email = 'john.doe@example.com',
#             Reporting_Manager = 2
#         )

#         # Set up the mock to return the application when queried
#         mock_query.get.return_value = application

#         # Call the method to test
#         result = self.manager.reject_application(100)

#         # Assertions
#         self.assertEqual(result, True)  # Check that it returns True
#         self.assertEqual(application.Status, 'Rejected')  # Check if the status was updated


#     @patch('extensions.db.Model.query')
#     def test_get_team_schedules(self, mock_query):
#         schedule1 = WFHSchedule(
#             Schedule_ID = 1,
#             Staff_ID = 1,
#             Application_ID = 1,
#             Team_ID = 2,
#             Date = datetime(2024, 10, 12, 6, 56, 4, 387232),
#             Time_Slot = "AM",
#             Status = "Approved",
#             Withdrawal_Reason = "",
#             Withdrawal_Confirmed = True,
#             Manager_Notified = True,
#         )
        
#         mock_filter_by = MagicMock()
#         mock_filter_by.all.return_value = [schedule1]
#         mock_query.filter_by.return_value = mock_filter_by
        
#         team_schedules = self.manager.get_team_schedules()
        
#         self.assertEqual(len(team_schedules), 1)
#         mock_query.filter_by.assert_called_once()
        

# if __name__ == '__main__':
#     unittest.main()
import unittest
import sys
import os
from unittest.mock import MagicMock, patch
from datetime import datetime
from models.Manager import Manager
from models.WFH_Application import WFHApplication

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
