import os
import requests
import unittest
from typing import List
from . import AutoGPTNewsSearch
from .news_search import news_search


class TestAutoGPTNewsSearch(unittest.TestCase):
    def setUp(self):
        os.environ["NEWSAPI_API_KEY"] = "test_key"
        self.plugin = AutoGPTNewsSearch()

    def tearDown(self):
        os.environ.pop("NEWSAPI_API_KEY", None)

    def test_news_search(self):
        query = "test query"
        try:
            news_search(query)
        except requests.exceptions.HTTPError as e:
            self.assertEqual(e.response.status_code, 401)

    def test_post_prompt(self):
        self.plugin = AutoGPTNewsSearch()

        prompt = self.plugin.post_prompt(
            "News Search", {"query": "AutoGPT"}
        )
        self.assertEqual(prompt, {"query": "AutoGPT"})

    def test_can_handle_pre_command(self):
        self.assertFalse(self.plugin.can_handle_pre_command())

    def test_can_handle_post_prompt(self):
        self.assertTrue(self.plugin.can_handle_post_prompt())


if __name__ == "__main__":
    unittest.main()
