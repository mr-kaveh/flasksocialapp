import os, sys

# Adds Module Path to the Python Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest # python Library 4 unitTesting

from user.tests import UserTest

if __name__ == '__main__':
    unittest.main()
