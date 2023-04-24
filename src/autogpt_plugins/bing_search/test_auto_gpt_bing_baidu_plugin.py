import os
import requests
import unittest
from typing import List
from . import AutoGPTBingSearch, _bing_search

class TestAutoGPTBingSearch(unittest.TestCase):

    def setUp(self):
        self.plugin = AutoGPTBingSearch()

    def test_bing_search(self):
        query = "test query"
        try:
            _bing_search(query)
        except requests.exceptions.HTTPError as e:
            self.assertEqual(e.response.status_code, 401)

    def test_pre_command(self):
        os.environ["AZURE_API_KEY"] = "test_key"
        os.environ["SEARCH_ENGINE"] = "bing"

        command_name, arguments = self.plugin.pre_command("google", {"query": "test query"})
        self.assertEqual(command_name, "execute_shell")
        self.assertEqual(arguments, {"command_line": "pwd"})

        os.environ.pop("SEARCH_ENGINE", None)
        command_name, arguments = self.plugin.pre_command("google", {"query": "test query"})
        self.assertEqual(command_name, "google")
        self.assertEqual(arguments, {"query": "test query"})

        command_name, arguments = self.plugin.pre_command("other_command", {})
        self.assertEqual(command_name, "other_command")
        self.assertEqual(arguments, {})

    def test_post_command(self):
        os.environ["AZURE_API_KEY"] = "test_key"
        self.plugin._query = "test query"
        with self.assertRaises(Exception):
            self.plugin.post_command("google", "")

        self.plugin._query = ""
        result = self.plugin.post_command("other_command", "")
        self.assertIsNone(result)

    def test_can_handle_pre_command(self):
        self.assertTrue(self.plugin.can_handle_pre_command())

    def test_can_handle_post_command(self):
        self.plugin.able_to_handle_post_command = True
        self.assertTrue(self.plugin.can_handle_post_command())

        self.plugin.able_to_handle_post_command = False
        self.assertFalse(self.plugin.can_handle_post_command())

if __name__ == '__main__':
    unittest.main()
