import os
import re
import requests

_engine_query_key = {
    "ebay": "_nkw",
    "google_maps_reviews": "data_id",
    "google_product": "product_id",
    "google_lens": "url",
    "google_immersive_product": "page_token",
    "google_scholar_author": "author_id",
    "google_scholar_profiles": "mauthors",
    "google_related_questions": "next_page_token",
    "google_finance_markets": "trend",
    "google_health_insurance": "provider_id",
    "home_depot_product": "product_id",
    "walmart": "query",
    "walmart_product": "product_id",
    "walmart_product_reviews": "product_id",
    "yahoo": "p",
    "yahoo_images": "p",
    "yahoo_videos": "p",
    "yandex": "text",
    "yandex_images": "text",
    "yandex_videos": "text",
    "youtube": "search_query",
    "google_play_product": "product_id",
    "yahoo_shopping": "p",
    "apple_app_store": "term",
    "apple_reviews": "product_id",
    "apple_product": "product_id",
    "naver": "query",
    "yelp": "find_desc",
    "yelp_reviews": "place_id",
}


def _filter_dict(obj, filter):
    if not isinstance(obj, dict):
        return obj

    return dict([(k, v) for k, v in obj.items() if k in filter])


def _filter_results(json, filterstr):
    if not filterstr or filterstr == "<none>":
        return json

    filter = {}
    matches = re.findall(r"(\w+)(?:\((.*?)\))*", filterstr)
    for match in matches:
        first_level = match[0]
        second_levels = [x.strip() for x in match[1].split(",") if x.strip() != ""]
        filter[first_level] = second_levels

    filtered_json = _filter_dict(json, list(filter.keys()))
    for k, v in filtered_json.items():
        inner_filter = filter[k]
        if len(inner_filter) > 0:
            if isinstance(v, list):
                filtered_json[k] = [
                    _filter_dict(x, inner_filter) for x in filtered_json[k]
                ]
            elif isinstance(v, dict):
                filtered_json[k] = _filter_dict(filtered_json[k], inner_filter)

    if len(filtered_json) == 1:
        return filtered_json[list(filtered_json.keys())[0]]
    return filtered_json


def _get_params(query: str):
    engine = os.getenv("SERPAPI_ENGINE") or "google"
    no_cache = os.getenv("SERPAPI_NO_CACHE")
    api_key = os.getenv("SERPAPI_API_KEY")
    params = {
        "engine": engine,
        "api_key": api_key,
        "source": "serpapi-auto-gpt-plugin-1st",
    }

    if no_cache and no_cache != "false":
        params["no_cache"] = "true"

    query_key = _engine_query_key[engine] if engine in _engine_query_key else "q"
    params[query_key] = query

    return params


def serpapi_search(query: str):
    """
    Perform a SerpApi search and return the JSON results.
    """

    response = requests.get("https://serpapi.com/search", params=_get_params(query))
    response.raise_for_status()

    result_json = response.json()

    filter = os.getenv("SERPAPI_RESULT_FILTER") or "organic_results(title,link,snippet)"
    return _filter_results(result_json, filter)
