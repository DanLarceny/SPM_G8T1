import unittest
from app import create_app, db
from models.Employee import Employee
from config import TestingConfig

class EmployeeModelIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app(TestingConfig)
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()


    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def test_employee_creation_and_retrieval(self):
        # Create a new employee
        new_employee = Employee(
            staff_f_name='Jane',
            staff_l_name='Smith',
            dept='HR',
            position='Manager',
            country='USA',
            email='jane.smith@example.com',
            reporting_manager=130002,
            role=1,
            password='securepassword'
        )
        db.session.add(new_employee)
        db.session.commit()

        # Retrieve the employee from the database
        retrieved_employee = Employee.query.filter_by(email='jane.smith@example.com').first()
        self.assertIsNotNone(retrieved_employee)
        self.assertEqual(retrieved_employee.staff_f_name, 'Jane')

if __name__ == '__main__':
    unittest.main()
