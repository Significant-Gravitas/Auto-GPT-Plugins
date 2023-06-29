import os
import unittest
from typing import List

import requests
import requests_mock

from . import AutoGPTSerpApiSearch
from .serpapi_search import serpapi_search, _filter_results, _get_params


class TestAutoGPTSerpApiSearch(unittest.TestCase):
    json_data = {
        "field1": 1,
        "field2": [1, 2, "3"],
        "field3": {"a": 1, "b": 2, "c": "3"},
        "field4": [
            {"a": 1, "b": 2, "c": "3"},
            {"a": 4, "b": 5, "c": "6"},
            7,
            False,
            {"a": 8, "b": "9", "c": 10},
        ],
        "organic_results": [
            {
                "title": "title 1",
                "link": "https://example1.com",
                "snippet": "snippet 1",
                "thumbnail": "https://path-to-thumbnail-1",
            },
            {
                "title": "title 2",
                "link": "https://example2.com",
                "snippet": "snippet 2",
                "thumbnail": "https://path-to-thumbnail-2",
            },
        ],
    }

    def setUp(self):
        os.environ["SERPAPI_API_KEY"] = "secret"
        self.plugin = AutoGPTSerpApiSearch()

    def tearDown(self):
        os.environ.pop("SERPAPI_API_KEY", None)
        os.environ.pop("SERPAPI_ENGINE", None)
        os.environ.pop("SERPAPI_NO_CACHE", None)
        os.environ.pop("SERPAPI_RESULT_FILTER", None)

    def test_pre_command(self):
        os.environ["SERPAPI_API_KEY"] = "secret"
        self.plugin = AutoGPTSerpApiSearch()

        command_name, arguments = self.plugin.pre_command(
            "google", {"query": "test query"}
        )
        self.assertEqual(command_name, "serpapi_search")
        self.assertEqual(arguments, {"query": "test query"})

    def test_can_handle_pre_command(self):
        self.assertTrue(self.plugin.can_handle_pre_command())

    def test_can_handle_post_prompt(self):
        self.assertTrue(self.plugin.can_handle_post_prompt())

    def test_filter_results_none(self):
        filtered = _filter_results(self.json_data, "<none>")
        self.assertDictEqual(filtered, self.json_data)

    def test_filter_results_top_level(self):
        filtered = _filter_results(self.json_data, "field1, field3")
        self.assertDictEqual(
            filtered, {"field1": 1, "field3": {"a": 1, "b": 2, "c": "3"}}
        )

    def test_filter_results_top_level_one_field(self):
        filtered = _filter_results(self.json_data, "field3")
        self.assertDictEqual(filtered, {"a": 1, "b": 2, "c": "3"})

    def test_filter_results_top_level_second_level_dict(self):
        filtered = _filter_results(self.json_data, "field1(a, b), field3(b, c)")
        self.assertDictEqual(filtered, {"field1": 1, "field3": {"b": 2, "c": "3"}})

    def test_filter_results_top_level_second_level_list(self):
        filtered = _filter_results(self.json_data, "field1(a, b), field4(b, c)")
        self.assertDictEqual(
            filtered,
            {
                "field1": 1,
                "field4": [
                    {"b": 2, "c": "3"},
                    {"b": 5, "c": "6"},
                    7,
                    False,
                    {"b": "9", "c": 10},
                ],
            },
        )

    def test_get_params_no_engine(self):
        params = _get_params("test query")
        self.assertDictEqual(
            params,
            {
                "engine": "google",
                "q": "test query",
                "api_key": "secret",
                "source": "serpapi-auto-gpt-plugin-1st",
            },
        )

    def test_get_params_engine_query_non_q(self):
        os.environ["SERPAPI_ENGINE"] = "yahoo"
        params = _get_params("test query")
        self.assertDictEqual(
            params,
            {
                "engine": "yahoo",
                "p": "test query",
                "api_key": "secret",
                "source": "serpapi-auto-gpt-plugin-1st",
            },
        )

    def test_get_params_no_cache_true(self):
        os.environ["SERPAPI_NO_CACHE"] = "true"
        params = _get_params("test query")
        self.assertDictEqual(
            params,
            {
                "engine": "google",
                "q": "test query",
                "no_cache": "true",
                "api_key": "secret",
                "source": "serpapi-auto-gpt-plugin-1st",
            },
        )

    def test_get_params_no_cache_false(self):
        os.environ["SERPAPI_NO_CACHE"] = "false"
        params = _get_params("test query")
        self.assertDictEqual(
            params,
            {
                "engine": "google",
                "q": "test query",
                "api_key": "secret",
                "source": "serpapi-auto-gpt-plugin-1st",
            },
        )

    @requests_mock.Mocker()
    def test_serpapi_search_default(self, m):
        m.get("https://serpapi.com/search", json=self.json_data)
        json = serpapi_search("test query")
        self.assertListEqual(
            json,
            [
                {
                    "title": "title 1",
                    "link": "https://example1.com",
                    "snippet": "snippet 1",
                },
                {
                    "title": "title 2",
                    "link": "https://example2.com",
                    "snippet": "snippet 2",
                },
            ],
        )

    @requests_mock.Mocker()
    def test_serpapi_search_custom_filter(self, m):
        os.environ["SERPAPI_RESULT_FILTER"] = "field1(a, b), field4(b, c)"
        m.get("https://serpapi.com/search", json=self.json_data)
        json = serpapi_search("test query")
        self.assertDictEqual(
            json,
            {
                "field1": 1,
                "field4": [
                    {"b": 2, "c": "3"},
                    {"b": 5, "c": "6"},
                    7,
                    False,
                    {"b": "9", "c": 10},
                ],
            },
        )


if __name__ == "__main__":
    unittest.main()
