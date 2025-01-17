import unittest
from Backend.WaitlistManager import WaitlistManager

class TestWaitlistManager(unittest.TestCase):
    def setUp(self):
        self.waitlist_manager = WaitlistManager()
        self.waitlist_manager.waitlist = []

    def test_add_to_waitlist(self):
        self.waitlist_manager.add_to_waitlist("Sample Book", "John Doe", "123456789", "john@example.com")
        self.assertEqual(len(self.waitlist_manager.waitlist), 1)
        self.assertEqual(self.waitlist_manager.waitlist[0]["Name"], "John Doe")

    def test_remove_from_waitlist(self):
        self.waitlist_manager.add_to_waitlist("Sample Book", "John Doe", "123456789", "john@example.com")
        removed_entry = self.waitlist_manager.remove_from_waitlist("Sample Book")
        self.assertEqual(removed_entry["Name"], "John Doe")
        self.assertEqual(len(self.waitlist_manager.waitlist), 0)
