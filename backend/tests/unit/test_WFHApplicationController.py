import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from controllers.WFHApplication import validate_dates, parse_date, create_application
from models.WFH_Application import WFHApplication

class TestWFHApplicationController(unittest.TestCase):

    def test_parse_date(self):
        date_str = "2024-10-18"
        expected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        parsed_date = parse_date(date_str)
        self.assertEqual(parsed_date, expected_date)

    def test_validate_dates(self):
        # Test past dates
        self.assertEqual(validate_dates(datetime.now().date() - timedelta(days=1), datetime.now().date()), "Cannot apply for past time blocks.")

        # Test start date after end date
        self.assertEqual(validate_dates(datetime.now().date() + timedelta(days=1), datetime.now().date()), "Start Date cannot be after End Date.")

        # Test date beyond one year
        self.assertEqual(validate_dates(datetime.now().date() + timedelta(days=366), datetime.now().date() + timedelta(days=366)), "Cannot apply for dates which are one year away from the present date.")

        # Test valid date range
        self.assertIsNone(validate_dates(datetime.now().date(), datetime.now().date() + timedelta(days=1)))

    @patch.object(WFHApplication, 'createApplication')
    def test_create_application(self, mock_create):
        mock_create.return_value = MagicMock(to_dict=lambda: {"success": True})

        # Test AdHoc application
        application = create_application("AdHoc", 130002, datetime.now().date(), datetime.now().date(), "PM", [], "test@example.com", "Reason", 130002)
        self.assertTrue(application.to_dict()["success"])

        # Test Recurring application
        application = create_application("Recurring", 130002, datetime.now().date(), datetime.now().date() + timedelta(days=1), "AM", ["Monday"], "test@example.com", "Reason", 130002)
        self.assertTrue(application.to_dict()["success"])

        # Test invalid application type
        application = create_application("InvalidType", 130002, datetime.now().date(), datetime.now().date() + timedelta(days=1), "AM", [], "test@example.com", "Reason", 130002)
        self.assertIsNone(application)

if __name__ == "__main__":
    unittest.main()
