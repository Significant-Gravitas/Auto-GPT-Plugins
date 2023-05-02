"""This module contains functions for interacting with the Bluesky API via atprototools."""
import pandas as pd
import os

from atprototools import Session


def username_and_pwd_set() -> bool:
    return True if os.getenv("BLUESKY_USERNAME") and os.getenv("BLUESKY_APP_PASSWORD") else False


def post_message(text: str) -> str:
    """Posts a message to Bluesky.

    Args:
        text (str): The message to post.

    Returns:
        str: The message that was posted.
    """

    bluesky_username = os.getenv("BLUESKY_USERNAME")
    bluesky_app_password = os.getenv("BLUESKY_APP_PASSWORD")
    session = Session(bluesky_username, bluesky_app_password)

    _result = session.post_bloot(text)

    if _result.status_code != 200:
        return f"Error! Status Code: {_result.status_code} Message: {_result.text}"

    return f"Success! Message: {text}"


def get_latest_posts(username: str, number_of_posts=5) -> str | None:
    """Gets the latest posts from a user.

    Args:
        username (str): The username to get the messages from.
        number_of_posts (int): The number of posts to get.

    Returns:
        str | None: The latest posts.
    """

    bluesky_username = os.getenv("BLUESKY_USERNAME")
    bluesky_app_password = os.getenv("BLUESKY_APP_PASSWORD")
    session = Session(bluesky_username, bluesky_app_password)

    _result = session.get_latest_n_bloots(username, number_of_posts)

    if _result.status_code != 200:
        return f"Error! Status Code: {_result.status_code} Message: {_result.text}"

    columns = ["URI", "Text", "Date", "User", "Likes", "Replies"]
    posts = []

    for bloot in _result.json()['feed']:
        posts.append([bloot['post']['uri'], bloot['post']['record']['text'], bloot['post']['record']['createdAt'],
                      bloot['post']['author']['handle'], bloot['post']['likeCount'], bloot['post']['replyCount']])

    df = str(pd.DataFrame(posts, columns=columns))

    print(df)

    return df
