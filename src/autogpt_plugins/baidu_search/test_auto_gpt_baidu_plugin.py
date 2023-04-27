import os
import requests
import unittest
from typing import List
from . import AutoGPTBaiduSearch
from .baidu_search import _baidu_search


class TestAutoGPTBaiduSearch(unittest.TestCase):
    def setUp(self):
        os.environ["BAIDU_COOKIE"] = "test_cookie"
        os.environ["SEARCH_ENGINE"] = "baidu"
        self.plugin = AutoGPTBaiduSearch()

    def tearDown(self):
        os.environ.pop("SEARCH_ENGINE", None)
        os.environ.pop("BAIDU_COOKIE", None)

    def test_baidu_search(self):
        query = "test query"
        try:
            _baidu_search(query)
        except requests.exceptions.HTTPError as e:
            self.assertEqual(e.response.status_code, 401)

    def test_pre_command(self):
        os.environ["SEARCH_ENGINE"] = "baidu"
        self.plugin = AutoGPTBaiduSearch()

        command_name, arguments = self.plugin.pre_command(
            "google", {"query": "test query"}
        )
        self.assertEqual(command_name, "baidu_search")
        self.assertEqual(arguments, {"query": "test query"})

    def test_can_handle_pre_command(self):
        self.assertTrue(self.plugin.can_handle_pre_command())

    def test_can_handle_post_prompt(self):
        self.assertTrue(self.plugin.can_handle_post_prompt())


if __name__ == "__main__":
    unittest.main()
