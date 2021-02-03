import unittest

from utils.logging_utils import configure_logs

if __name__ == '__main__':
    configure_logs()
    test_suite = unittest.TestLoader().discover('functional')
    unittest.TextTestRunner().run(test_suite)
