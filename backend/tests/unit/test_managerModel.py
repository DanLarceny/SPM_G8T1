import unittest
import sys
import os
# Add backend to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from unittest.mock import MagicMock, patch
from models.Manager import Manager
from models.WFH_Application import WFHApplication
from models.WFH_Schedule import WFHSchedule
from datetime import datetime

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


    @patch('extensions.db.session.commit')
    @patch('extensions.db.Model.query')
    def test_approve_application(self, mock_query, mock_commit):
        application = WFHApplication(
            Application_ID = 100,
            Staff_ID = 1,
            Start_Date = datetime(2024, 10, 12, 6, 56, 4, 387232),
            End_Date = datetime(2025, 10, 12, 6, 56, 4, 387232),
            Status = 'Pending',
            Time_Slot = 'Day',
            Type = 'Recurring',
            Email = 'john.doe@example.com',
            Reporting_Manager = 2
        )

        # Set up the mock to return the application when queried
        mock_query.get.return_value = application

        # Create a Manager instance with the corresponding Staff_ID
        manager = Manager()
        manager.Staff_ID = 2  # Ensure this matches Reporting_Manager

        # Call the method to test
        result = manager.approve_application(100)

        # Assertions
        self.assertEqual(result, True)  # Check that it returns True
        self.assertEqual(application.Status, 'Approved')  # Check if the status was updated

    @patch('extensions.db.session.commit')
    @patch('extensions.db.Model.query')
    def test_reject_application(self, mock_query, mock_commit):
        application = WFHApplication(
            Application_ID = 100,
            Staff_ID = 1,
            Start_Date = datetime(2024, 10, 12, 6, 56, 4, 387232),
            End_Date = datetime(2025, 10, 12, 6, 56, 4, 387232),
            Status = 'Pending',
            Time_Slot = 'Day',
            Type = 'Recurring',
            Email = 'john.doe@example.com',
            Reporting_Manager = 2
        )

        # Set up the mock to return the application when queried
        mock_query.get.return_value = application

        # Call the method to test
        result = self.manager.reject_application(100)

        # Assertions
        self.assertEqual(result, True)  # Check that it returns True
        self.assertEqual(application.Status, 'Rejected')  # Check if the status was updated


    @patch('extensions.db.Model.query')
    def test_get_team_schedules(self, mock_query):
        schedule1 = WFHSchedule(
            Schedule_ID = 1,
            Staff_ID = 1,
            Application_ID = 1,
            Team_ID = 2,
            Date = datetime(2024, 10, 12, 6, 56, 4, 387232),
            Time_Slot = "AM",
            Status = "Approved",
            Withdrawal_Reason = "",
            Withdrawal_Confirmed = True,
            Manager_Notified = True,
        )
        
        mock_filter_by = MagicMock()
        mock_filter_by.all.return_value = [schedule1]
        mock_query.filter_by.return_value = mock_filter_by
        
        team_schedules = self.manager.get_team_schedules()
        
        self.assertEqual(len(team_schedules), 1)
        mock_query.filter_by.assert_called_once()
        

if __name__ == '__main__':
    unittest.main()
