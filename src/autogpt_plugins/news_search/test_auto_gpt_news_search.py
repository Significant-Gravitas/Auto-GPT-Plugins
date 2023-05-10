import json
from unittest.mock import Mock

import pytest

from .news_search import NewsSearch


class TestNewsSearch:
    def mock_response(self, *args, **kwargs):
        # Mock Response of NewsAPI. We have result for AutoGPT in technology but not others,
        # whereas Cricket is present in Sports/Entertainment but not others
        if kwargs["q"] == "AI" and kwargs["category"] == "technology":
            return json.loads(
                """{"status":"ok","totalResults":1,"articles": [{"title": "AutoGPT"}]}"""
            )
        elif kwargs["q"] == "Cricket" and kwargs["category"] in [
            "entertainment",
            "sports",
        ]:
            return json.loads(
                """{"status":"ok","totalResults":1,"articles": [{"title": "World Cup"}]}"""
            )
        elif kwargs["q"] == "Taylor Swift":
            return json.loads(
                """{"status": "ok","totalResults": 1,"articles": [{"title": "The National enlist Taylor Swift for new song “The Alcott”"}]}"""
            )
        else:
            return json.loads("""{"status":"ok","totalResults":0,"articles":[]}""")

    @pytest.fixture(autouse=True)
    def setUp(self):
        self.NewsSearch = NewsSearch("testKey")
        self.NewsSearch.news_api_client.get_top_headlines = Mock(
            side_effect=self.mock_response
        )
        self.NewsSearch.news_api_client.get_everything = Mock(
            side_effect=self.mock_response
        )

    def test_news_search(self):
        # For AI, only technology should be populated. However, we can't rely on ordering,
        # so we'll assert one actual answer and 5 empty answers
        actual_output_autogpt = self.NewsSearch.news_headlines_search_wrapper("AI")
        assert actual_output_autogpt.count(["AutoGPT"]) == 1
        assert actual_output_autogpt.count([]) == 5

        # For Cricket, we should have sports/entertainment
        actual_output_cricket = self.NewsSearch.news_headlines_search_wrapper("Cricket")
        assert actual_output_cricket.count(["World Cup"]) == 2
        assert actual_output_cricket.count([]) == 4

        actual_output_taylor = self.NewsSearch.news_everything_search("Taylor Swift")
        assert actual_output_taylor.count(["Taylor Swift"]) == 0
        assert actual_output_taylor.count([]) == 0
