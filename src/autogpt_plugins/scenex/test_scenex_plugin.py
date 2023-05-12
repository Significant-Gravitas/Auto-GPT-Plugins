import os
import unittest
from unittest.mock import MagicMock, patch

from .scenex_plugin import SceneXplain

MOCK_API_KEY = "secret"
MOCK_IMAGE = "https://example.com/image.png"
MOCK_DESCRIPTION = "example description"


class TestEmailPlugin(unittest.TestCase):
    @patch("scenex_plugin.requests.post")
    def test_describe_image(self, mock_post):
        mock_post.return_value = MagicMock(
            json=MagicMock(
                return_value={
                    "result": [
                        {
                            "image": MOCK_IMAGE,
                            "text": MOCK_DESCRIPTION,
                        }
                    ]
                }
            )
        )

        scenex = SceneXplain(MOCK_API_KEY)
        result = scenex.describe_image(
            image=MOCK_IMAGE,
            algorithm="Dune",
            features=[],
            languages=[],
        )

        # Check the results
        self.assertEqual(
            result,
            {
                "image": MOCK_IMAGE,
                "description": MOCK_DESCRIPTION,
            },
        )

        # Check that the mocked functions were called with the correct arguments
        mock_post.assert_called_once_with(
            "https://us-central1-causal-diffusion.cloudfunctions.net/describe",
            headers={
                "x-api-key": f"token {MOCK_API_KEY}",
                "content-type": "application/json",
            },
            json={
                "data": [
                    {
                        "image": MOCK_IMAGE,
                        "algorithm": "Dune",
                        "features": [],
                        "languages": [],
                    }
                ]
            },
        )


if __name__ == "__main__":
    unittest.main()
