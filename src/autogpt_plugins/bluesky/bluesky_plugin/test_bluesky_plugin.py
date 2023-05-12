import os
from .bluesky_plugin import (
    username_and_pwd_set,
    post_message,
    get_latest_posts,
)
import unittest

MOCK_USERNAME = "example.bsky.social"
MOCK_MESSAGE = "Hello, World!"


class TestBlueskyPlugin(unittest.TestCase):
    def setUp(self):
        os.environ["BLUESKY_USERNAME"] = "example.bsky.social"
        os.environ["BLUESKY_APP_PASSWORD"] = "bsky-social-app-password"

    def tearDown(self):
        os.environ.pop("BLUESKY_USERNAME", None)
        os.environ.pop("BLUESKY_APP_PASSWORD", None)

    def test_username_and_pwd_set(self):
        self.assertTrue(username_and_pwd_set())

    def test_post_message(self):
        self.assertIsInstance(post_message(MOCK_MESSAGE), str)

    def test_get_latest_posts(self):
        self.assertIsInstance(get_latest_posts(MOCK_USERNAME, 5), str)


if __name__ == "__main__":
    unittest.main()
