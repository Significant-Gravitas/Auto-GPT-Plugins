import os
import unittest

import requests

from . import AutoGPTWolframAlphaSearch
from . import _wolframalpha_search


class TestAutoGPTWolframAlphaSearch(unittest.TestCase):
    def setUp(self):
        os.environ["WOLFRAMALPHA_APPID"] = "test_appid"
        self.plugin = AutoGPTWolframAlphaSearch()

    def tearDown(self):
        os.environ.pop("WOLFRAMALPHA_APPID", None)

    def test_bing_search(self):
        query = "2+2"
        try:
            _wolframalpha_search(query)
        except requests.exceptions.HTTPError as e:
            self.assertEqual(e.response.status_code, 401)


if __name__ == "__main__":
    unittest.main()
