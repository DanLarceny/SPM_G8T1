import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import unittest
from unittest.mock import MagicMock, patch
from models.Role import Role


class TestRoleModel(unittest.TestCase):

    def setUp(self):
        
        self.role = Role(
            Role=1,
            Role_Name='HR/Director'
        )
        repr(self.role)
        
    def test_get_role(self):
        # Create a mock query result
        self.assertEqual(repr(self.role), "<Role 1 - HR/Director>")


if __name__ == '__main__':
    unittest.main()
