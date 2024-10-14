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
            Start_Date = datetime(2023, 1, 1),
            End_Date = datetime(2023, 1, 7),
            Status = "pending" 
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
    
    def test_invalid_dates(self):
        with self.assertRaises(ValueError):
            WFHApplication(
                Application_ID=2,
                Staff_ID=101,
                Start_Date=datetime(2023, 1, 7),
                End_Date=datetime(2023, 1, 1),
                Status="Pending"
            )
    
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
    
    def test_approve_case_insensitive(self):
        self.application.Status = "PENDING"
        self.application.approve()
        self.assertEqual(self.application.Status, "Approved")

        self.application.Status = "pending"
        self.application.approve()
        self.assertEqual(self.application.Status, "Approved")


if __name__ == '__main__':
    unittest.main()