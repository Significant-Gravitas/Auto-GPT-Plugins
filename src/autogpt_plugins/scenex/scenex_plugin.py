import requests
from typing import List, Union


Algorithm = Union["Aqua", "Bolt", "Comet", "Dune", "Ember", "Flash"]


class SceneXplain:
    API_ENDPOINT = "https://us-central1-causal-diffusion.cloudfunctions.net/describe"

    def __init__(self, api_key):
        self._api_key = api_key

    def describe_image(
        self,
        image: str,
        algorithm: Algorithm = "Dune",
        features: List[str] = [],
        languages: List[str] = [],
    ) -> str:
        headers = {
            "x-api-key": f"token {self._api_key}",
            "content-type": "application/json",
        }

        payload = {
            "data": [
                {
                    "image": image,
                    "algorithm": algorithm,
                    "features": features,
                    "languages": languages,
                }
            ]
        }

        response = requests.post(self.API_ENDPOINT, headers=headers, json=payload)
        result = response.json().get("result", [])
        img = result[0] if result else {}

        return {"image": image, "description": img.get("text", "")}
