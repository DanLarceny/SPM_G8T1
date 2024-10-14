import unittest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import sys
import os
# Add backend to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from models.Employee import Employee
from models.WFH_Schedule import WFHSchedule
from models.WFH_Application import WFHApplication



class TestWFHScheduleModel(unittest.TestCase):
    def setUp(self): 
        self.staff_id = 1
        self.application_id = 100
        self.valid_date = datetime.now() + timedelta(days=2)  # Valid future date
        self.valid_time_slot = 'AM'
    
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
    
    # @patch('extensions.db.session.add')
    # @patch('extensions.db.session.commit')
    # @patch('extensions.db.session.rollback')
    # def test_update_schedule_happy_path(self):
    #     new_time_slot = 'PM'
    #     new_date = datetime.now() + timedelta(days=3)
    #     updated_schedule = WFHSchedule.updateSchedule(self.schedule.Schedule_ID, new_time_slot, new_date)
    #     self.assertEqual(updated_schedule.Time_Slot, new_time_slot)
    #     self.assertEqual(updated_schedule.Date, new_date)

    # @patch('extensions.db.session.add')
    # @patch('extensions.db.session.commit')
    # @patch('extensions.db.session.rollback')
    # def test_update_schedule_invalid_date(self):
    #     with self.assertRaises(ValueError) as context:
    #         WFHSchedule.updateSchedule(self.schedule.Schedule_ID, 'PM', datetime.now().date())
    #     self.assertEqual(str(context.exception), "Invalid date. Date must be in the future.")

    # @patch('extensions.db.session.add')
    # @patch('extensions.db.session.commit')
    # @patch('extensions.db.session.rollback')
    # def test_update_schedule_schedule_not_found(self):
    #     with self.assertRaises(ValueError) as context:
    #         WFHSchedule.updateSchedule(999, 'PM', datetime.now() + timedelta(days=1))
    #     self.assertEqual(str(context.exception), "Schedule not found")