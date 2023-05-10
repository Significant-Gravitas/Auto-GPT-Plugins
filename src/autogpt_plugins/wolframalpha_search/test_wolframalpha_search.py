import os
import unittest

import requests

from . import AutoGPTWolframAlphaSearch


class TestAutoGPTWolframAlphaSearch(unittest.TestCase):
    def setUp(self):
        os.environ["WOLFRAMALPHA_APPID"] = "test_appid"
        self.plugin = AutoGPTWolframAlphaSearch()

    def tearDown(self):
        os.environ.pop("WOLFRAMALPHA_APPID", None)

    def test_wolframalpha_search(self):
        query = "2+2"
        try:
            from .wolframalpha_search import _wolframalpha_search
            _wolframalpha_search(query)
        except requests.exceptions.HTTPError as e:
            self.assertEqual(e.response.status_code, 401)


if __name__ == "__main__":
    unittest.main()
