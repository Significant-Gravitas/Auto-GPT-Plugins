import unittest
from unittest.mock import Mock, patch
try:
    from .chat_with_user import ChatWithUserPlugin
except ImportError:
    from chat_with_user import ChatWithUserPlugin

class TestChatWithUser(unittest.TestCase):
    
    def setUp(self):
        self.plugin = ChatWithUserPlugin('Test Plugin')

    def test_clean_string(self):
        dirty_string = 'Hello\x00 World\x01'
        expected_clean_string = 'Hello World'
        self.assertEqual(self.plugin.clean_string(dirty_string), expected_clean_string)

    def test_handle_new_message(self):
        self.plugin.handle_new_message('Hello')
        self.assertEqual(self.plugin.message, 'Hello')

    def test_handle_window_close(self):
        self.plugin.handle_window_close()
        self.assertEqual(self.plugin.message, 'User closed the window.')

