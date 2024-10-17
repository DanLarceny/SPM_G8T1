import unittest
from unittest.mock import patch, MagicMock
from flask_testing import TestCase
from extensions import db
from models.Employee import Employee
from models.WFHApplication import WFHApplication  # Assuming this is where your model is defined
from config import TestingConfig
from app import create_app
from datetime import datetime, timedelta

class TestWFHApplicationModel(TestCase):
    def create_app(self):
        app = create_app(TestingConfig)
        return app

    def setUp(self):
        db.create_all()
        
        # Create a test manager who is also an employee
        self.test_manager = Employee(
            Staff_ID=1,
            Staff_FName='Test',
            Staff_LName='Manager',
            Dept='Management',
            Position='Manager',
            Country='USA',
            Email='manager@example.com',
            Reporting_Manager=None,  # No reporting manager for the top-level manager
            Role=1,  # Assuming Role ID exists
            Password='securepassword'
        )
        db.session.add(self.test_manager)
        db.session.commit()

        # Create a test employee
        self.test_employee = Employee(
            Staff_ID=2,
            Staff_FName='John',
            Staff_LName='Doe',
            Dept='Engineering',
            Position='Developer',
            Country='USA',
            Email='john.doe@example.com',
            Reporting_Manager=self.test_manager.Staff_ID,
            Role=1,  # Assuming Role ID exists
            Password='securepassword'
        )
        db.session.add(self.test_employee)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    @patch('models.WFHApplication.db.session')  # Mock the db session
    def test_create_application(self, mock_session):
        # Arrange
        start_date = datetime.now()
        end_date = start_date + timedelta(days=5)
        time_slot = 'AM'
        selected_days = ['Mon', 'Tue', 'Wed']
        email = 'john.doe@example.com'
        reason = 'Personal reasons'
        type = 'AdHoc'
        
        # Act
        application = WFHApplication.createApplication(
            staff_id=self.test_employee.Staff_ID,
            start_date=start_date,
            end_date=end_date,
            time_slot=time_slot,
            selected_days=selected_days,
            email=email,
            reason=reason,
            type=type,
            reporting_manager=self.test_manager.Staff_ID
        )

        # Assert
        self.assertIsNotNone(application.Application_ID)
        self.assertEqual(application.Staff_ID, self.test_employee.Staff_ID)
        self.assertEqual(application.Status, 'Pending')
        self.assertEqual(application.Time_Slot, time_slot)
        self.assertEqual(application.Type, type)
        self.assertEqual(application.Email, email)
        self.assertEqual(application.Reporting_Manager, self.test_manager.Staff_ID)
        self.assertEqual(application.Days, 'Monday,Tuesday,Wednesday')

        mock_session.add.assert_called_once_with(application)
        mock_session.commit.assert_called_once()

    @patch('models.WFHApplication.db.session')  # Mock the db session
    def test_approve_application(self, mock_session):
        # Arrange
        application = WFHApplication(
            Staff_ID=self.test_employee.Staff_ID,
            Start_Date=datetime.now(),
            End_Date=datetime.now() + timedelta(days=5),
            Status='Pending',
            Time_Slot='AM',
            Type='AdHoc',
            Email=self.test_employee.Email,
            Reporting_Manager=self.test_manager.Staff_ID,
            Days='Monday,Tuesday',
            Reason='Personal reasons'
        )
        db.session.add(application)
        db.session.commit()

        # Act
        application.approve()

        # Assert
        self.assertEqual(application.Status, 'Approved')
        mock_session.commit.assert_called()

    @patch('models.WFHApplication.db.session')  # Mock the db session
    def test_reject_application(self, mock_session):
        # Arrange
        application = WFHApplication(
            Staff_ID=self.test_employee.Staff_ID,
            Start_Date=datetime.now(),
            End_Date=datetime.now() + timedelta(days=5),
            Status='Pending',
            Time_Slot='AM',
            Type='AdHoc',
            Email=self.test_employee.Email,
            Reporting_Manager=self.test_manager.Staff_ID,
            Days='Monday,Tuesday',
            Reason='Personal reasons'
        )
        db.session.add(application)
        db.session.commit()

        # Act
        application.reject()

        # Assert
        self.assertEqual(application.Status, 'Rejected')
        mock_session.commit.assert_called()

    @patch('models.WFHApplication.db.session')  # Mock the db session
    def test_approve_rejected_application(self, mock_session):
        # Arrange
        application = WFHApplication(
            Staff_ID=self.test_employee.Staff_ID,
            Start_Date=datetime.now(),
            End_Date=datetime.now() + timedelta(days=5),
            Status='Rejected',
            Time_Slot='AM',
            Type='AdHoc',
            Email=self.test_employee.Email,
            Reporting_Manager=self.test_manager.Staff_ID,
            Days='Monday,Tuesday',
            Reason='Personal reasons'
        )
        db.session.add(application)
        db.session.commit()

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            application.approve()
        self.assertEqual(str(context.exception), "Cannot approve a rejected application")

if __name__ == '__main__':
    unittest.main()
