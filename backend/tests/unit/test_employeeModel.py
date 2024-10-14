import unittest
import sys
import os
# Add backend to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from unittest.mock import MagicMock, patch
from models.Employee import Employee
from models.WFH_Schedule import WFHSchedule

class TestEmployeeModel(unittest.TestCase):
    def setUp(self):
        self.employee = Employee(
            Staff_ID=1,
            Staff_FName='John',
            Staff_LName='Doe',
            Dept='IT',
            Position='Developer',
            Country='USA',
            Email='john.doe@example.com',
            Reporting_Manager=2,
            Role=1,
            Password='hashed_password'
        )
    
    def test_get_own_schedules(self):
        self.employee.schedules = [MagicMock(), MagicMock()]
        own_schedules = self.employee.getOwnSchedules()
        self.assertEqual(len(own_schedules), 2)
    
    
    @patch('extensions.db.Model.query')
    def test_get_team_schedules(self, mock_query):
        team_member = MagicMock()
        team_member.Staff_ID = self.employee.Staff_ID
        team_member.schedules = [MagicMock(), MagicMock()]
        
        mock_query.filter.return_value.all.return_value = [team_member]
        
        team_schedules = self.employee.get_team_schedules()
        
        self.assertEqual(len(team_schedules), 2)
        mock_query.filter.assert_called_once()
    
    def test_get_applications(self):
        self.employee.applications = [MagicMock(), MagicMock()]
        applications = self.employee.getApplications()
        self.assertEqual(len(applications), 2)
    
    @patch('extensions.db.session.commit')
    def test_withdraw_schedule(self, mock_commit):
        mockSchedule1 = MagicMock()  
        mockSchedule1.Schedule_ID = 1
        mockSchedule1.status = 'Upcoming'
        mockSchedule2 = MagicMock()
        mockSchedule2.Schedule_ID = 2
        mockSchedule2.status = 'Upcoming'
        self.employee.schedules = [mockSchedule1, mockSchedule2]
        
        res = self.employee.withdrawSchedule(1)
        
        self.assertEqual(mockSchedule2.status, 'Upcoming')
        mock_commit.assert_called_once()
        self.assertEqual(mockSchedule1.status, 'Cancelled')
        self.assertEqual(res, True)
    
    def test_withdraw_schedule_not_found(self):
        res = self.employee.withdrawSchedule(999)
        self.assertEqual(res, False)
    
    @patch('extensions.db.session.commit')
    def test_withdraw_application(self, mock_commit):
        mockApplication1 = MagicMock()
        mockApplication1.Application_ID = 1
        mockApplication1.status = 'Pending'
        mockApplication2 = MagicMock()
        mockApplication2.Application_ID = 2
        mockApplication2.status = 'Pending' 
        self.employee.applications = [mockApplication1, mockApplication2]
        
        res = self.employee.withdrawApplication(1)
        
        self.assertEqual(mockApplication2.status, 'Pending')
        mock_commit.assert_called_once()
        self.assertEqual(mockApplication1.status, 'Withdrawn')
        self.assertEqual(res, True)
    
    def test_withdraw_application_not_found(self):
        res = self.employee.withdrawApplication(999)
        self.assertEqual(res, False)
    
if __name__ == '__main__':
    unittest.main()
