import unittest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import sys
import os
# Add backend to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from extensions import db
from app import create_app

from models.Employee import Employee
from models.WFH_Schedule import WFHSchedule
from models.WFH_Application import WFHApplication

class TestWFHScheduleModel(unittest.TestCase):
    def setUp(self): 
        """Set up the test case with necessary variables and context."""
        self.app = create_app()  # Use the imported Flask app instance
        self.app_context = self.app.app_context()
        self.app_context.push()  # Push the app context to make it active

        self.schedule_id = 1
        self.staff_id = 1
        self.application_id = 100
        self.valid_date = datetime.now() + timedelta(days=2)  # Valid future date
        self.valid_time_slot = 'AM'
        self.status = "Upcoming"

        # Sample schedule object for testing
        self.schedule = WFHSchedule(
            Schedule_ID=self.schedule_id,
            Staff_ID=self.staff_id,
            Application_ID=self.application_id,
            Date=self.valid_date,
            Time_Slot=self.valid_time_slot,
            Status='Upcoming'
        )
    
    #Test create_schedule
    @patch('extensions.db.session.commit')
    @patch('extensions.db.session.add')
    @patch('extensions.db.session.rollback')
    def test_create_schedule_happy_path(self, mock_rollback, mock_add, mock_commit):
        result = WFHSchedule.createSchedule(
            staff_id=self.staff_id,
            application_id=self.application_id,
            date=self.valid_date,
            time_slot=self.valid_time_slot
        )

        self.assertIsInstance(result, WFHSchedule)
        self.assertEqual(result.Staff_ID, self.staff_id)
        self.assertEqual(result.Application_ID, self.application_id)
        self.assertEqual(result.Date, self.valid_date)
        self.assertEqual(result.Time_Slot, self.valid_time_slot)
        self.assertEqual(result.Status, 'Upcoming')

        mock_add.assert_called_once()
        mock_commit.assert_called_once()
        mock_rollback.assert_not_called()

    @patch('extensions.db.session.rollback')
    def test_create_schedule_past_date(self, mock_rollback):
        past_date = datetime.now().date() - timedelta(days=1)
        
        with self.assertRaises(ValueError) as context:
            WFHSchedule.createSchedule(
                staff_id=self.staff_id,
                application_id=self.application_id,
                date=past_date,
                time_slot=self.valid_time_slot
            )
        
        self.assertTrue("Invalid date. Date must be in the future." in str(context.exception))
        mock_rollback.assert_called_once()
    
    @patch('extensions.db.session.rollback')
    def test_create_schedule_far_future_date(self, mock_rollback):
        far_future_date = datetime.now().date() + timedelta(days=366)
        
        with self.assertRaises(ValueError) as context:
            WFHSchedule.createSchedule(
                staff_id=self.staff_id,
                application_id=self.application_id,
                date=far_future_date,
                time_slot=self.valid_time_slot
            )
        
        self.assertTrue("Invalid date. Date must be within one year." in str(context.exception))
        mock_rollback.assert_called_once()

    @patch('extensions.db.session.add')
    @patch('extensions.db.session.commit')
    @patch('extensions.db.session.rollback')
    def test_create_schedule_database_error(self, mock_rollback, mock_commit, mock_add):
        mock_commit.side_effect = Exception("Database error")


    #Testing cancel_withdraw_method
    @patch('extensions.db.session.commit')
    @patch('models.WFH_Schedule.WFHSchedule.query')
    def test_cancel_schedule_happy_path(self, mock_query, mock_commit):
        # Mock the query to return a valid schedule
        mock_query.get.return_value = self.schedule

        result = WFHSchedule.cancelSchedule(self.schedule_id)
        self.assertEqual(result.Status, 'Cancelled')

        mock_commit.assert_called_once()


    @patch('extensions.db.session.rollback')
    @patch('models.WFH_Schedule.WFHSchedule.query')
    def test_cancel_schedule_not_found(self, mock_query, mock_rollback):
        # Mock the query to return None (no schedule found)
        mock_query.get.return_value = None

        with self.assertRaises(ValueError) as context:
            WFHSchedule.cancelSchedule(self.schedule_id)

        self.assertTrue("Schedule not found" in str(context.exception))
        mock_rollback.assert_called_once()

    @patch('extensions.db.session.commit')
    @patch('extensions.db.session.rollback')
    @patch('models.WFH_Schedule.WFHSchedule.query')
    def test_cancel_schedule_database_error(self, mock_query, mock_rollback, mock_commit):
        # Mock the query to return a valid schedule
        mock_query.get.return_value = self.schedule
        # Simulate a database error
        mock_commit.side_effect = Exception("Database error")

        with self.assertRaises(Exception) as context:
            WFHSchedule.cancelSchedule(self.schedule_id)

        self.assertTrue("Database error" in str(context.exception))
        mock_rollback.assert_called_once()
    
    # #Test update schedule method
    # @patch('extensions.db.session.commit')
    # @patch('models.WFH_Schedule.WFHSchedule.query')
    # def test_update_schedule_happy_path(self, mock_query, mock_commit):
    #     """Test successfully updating the schedule."""
    #     # Mock the query to return a valid schedule
    #     mock_query.get.return_value = self.schedule

    #     result = WFHSchedule.updateSchedule(
    #         schedule_id=self.schedule_id, 
    #         time_slot=self.valid_time_slot, 
    #         date=self.valid_date.date()
    #     )

    #     self.assertEqual(result.Time_Slot, self.valid_time_slot)
    #     self.assertEqual(result.Date, self.valid_date.date())
    #     mock_commit.assert_called_once()
    
    @patch('extensions.db.session.rollback')
    @patch('models.WFH_Schedule.WFHSchedule.query')
    def test_update_schedule_not_found(self, mock_query, mock_rollback):
        """Test updating a non-existent schedule."""
        # Mock the query to return None (no schedule found)
        mock_query.get.return_value = None

        with self.assertRaises(ValueError) as context:
            WFHSchedule.updateSchedule(
                schedule_id=self.schedule_id, 
                time_slot=self.valid_time_slot, 
                date=self.valid_date.date()
            )

        self.assertIn("Schedule not found", str(context.exception))
        mock_rollback.assert_called_once()

    #Test can_withdraw method
    def test_can_withdraw_happy_path(self):
        # Valid case: more than 24 hours before the start date
        self.schedule.Date = datetime.now() + timedelta(days=2)  # Future date
        result = self.schedule.can_withdraw()
        self.assertTrue(result)

    def test_can_withdraw_negative_case(self):
        # Edge case: less than 24 hours before the start date
        self.schedule.Date= datetime.now() + timedelta(hours=23)  # Just inside the 24-hour limit
        result = self.schedule.can_withdraw()
        self.assertFalse(result)
    
    def test_can_withdraw_exact_boundary(self):
        # Boundary case: exactly 24 hours before the start date
        self.schedule.Date = datetime.now() + timedelta(hours=24)
        result = self.schedule.can_withdraw()
        self.assertTrue(result)

    #test withdraw method
    @patch('extensions.db.session.commit')
    def test_withdraw_happy_path(self, mock_commit):
        # Ensure schedule is withdrawable (more than 24 hours before start)
        self.schedule.Date = datetime.now() + timedelta(days=2)

        # Call withdraw method with a reason
        self.schedule.withdraw(reason="Personal reason")

        self.assertEqual(self.schedule.Status, 'Withdrawn')
        self.assertEqual(self.schedule.Withdrawal_Reason, "Personal reason")
        mock_commit.assert_called_once()

    def test_withdraw_within_24_hours(self):
        # Ensure schedule is NOT withdrawable (less than 24 hours before start)
        self.schedule.Date = datetime.now() + timedelta(hours=23)

        with self.assertRaises(ValueError) as context:
            self.schedule.withdraw(reason="Personal reason")

        self.assertTrue("Cannot withdraw a schedule within 24 hours" in str(context.exception))

if __name__ == '__main__':
    unittest.main()