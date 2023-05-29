from .scenex_plugin import SceneXplain

MOCK_API_KEY = "secret"
MOCK_IMAGE = "https://example.com/image.png"
MOCK_DESCRIPTION = "example description"


def test_describe_image(requests_mock):
    requests_mock.post(
        SceneXplain.API_ENDPOINT,
        json={
            "result": [
                {
                    "image": MOCK_IMAGE,
                    "text": MOCK_DESCRIPTION,
                }
            ]
        },
    )

    scenex = SceneXplain(MOCK_API_KEY)
    result = scenex.describe_image(
        image=MOCK_IMAGE,
        algorithm="Dune",
        features=[],
        languages=[],
    )

    # Check the results
    assert result == {
        "image": MOCK_IMAGE,
        "description": MOCK_DESCRIPTION,
    }

    # Check that the mocked functions were called with the correct arguments
    requests_mock.request_history[0].json() == {
        "data": [
            {
                "image": MOCK_IMAGE,
                "algorithm": "Dune",
                "features": [],
                "languages": [],
            }
        ]
    }
