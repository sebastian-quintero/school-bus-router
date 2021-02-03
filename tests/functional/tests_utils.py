import unittest

from utils.time_utils import hour_to_sec


class TestsUtils(unittest.TestCase):
    """Tests for the project's utils"""

    def test_hour_to_sec(self):
        """Asserts hours are parsed correctly"""

        hours = 2
        sec = hour_to_sec(hours)
        self.assertEqual(sec, hours * 3600, msg='Hours parsed incorrectly.')
