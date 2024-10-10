import unittest
from unittest.mock import MagicMock, patch
from models.Manager import Manager
from models.WFH_Schedule import WFHSchedule

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
            Role=2,
            Password='hashed_password'
        )

    @patch('extensions.db.session.commit')
    @patch('extensions.db.Model.query')
    def test_approve_application(self, mock_get, mock_commit):
        # Mock a WFHApplication object with the right conditions
        application = MagicMock()
        application.application_id = 100
        application.status = 'Pending'
        application.reporting_manager = 2

        # Set up the mock to return the application when queried
        mock_get.return_value = application
        
        # Call the method to test
        result = self.manager.approve_application(100)
        
        # Assertions
        self.assertEqual(result, True)  # Check that it returns True
        application.approve.assert_called_once()  # Ensure that the approve method was called
        mock_commit.assert_called_once()  # Check that the commit was called once
        mock_get.assert_called_once_with(100)  # Ensure the get was called with the correct ID



        
if __name__ == '__main__':
    unittest.main()
