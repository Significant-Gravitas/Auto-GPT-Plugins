import os
import json
import requests
import unittest
from unittest.mock import MagicMock
from typing import List
from . import AutoGPTBingBaiduSearch, baidu_search, _bing_search

class TestAutoGPTBingBaiduSearch(unittest.TestCase):

    def setUp(self):
        self.plugin = AutoGPTBingBaiduSearch()

    def test_baidu_search(self):
        query = "test query"
        result = baidu_search(query)
        search_results = json.loads(result)
        self.assertEqual(search_results, [])

    def test_bing_search(self):
        query = "test query"
        try:
            _bing_search(query)
        except requests.exceptions.HTTPError as e:
            self.assertEqual(e.response.status_code, 401)

    def test_pre_command(self):
        os.environ["AZURE_API_KEY"] = "test_key"
        command_name, arguments = self.plugin.pre_command("google", {"query": "test query"})
        self.assertEqual(command_name, "execute_shell")
        self.assertEqual(arguments, {"command_line": "pwd"})

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
