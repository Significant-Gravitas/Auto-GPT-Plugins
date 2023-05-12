"""This module contains functions for interacting with the Bluesky API via atprototools."""
import pandas as pd
import os

from atproto import Client


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

    client = Client()

    try:
        client.login(bluesky_username, bluesky_app_password)
        client.send_post(text=text)
    except Exception as e:
        return f"Error! Message: {e}"

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

    client = Client()

    try:
        client.login(bluesky_username, bluesky_app_password)
        profile_feed = client.bsky.feed.get_author_feed(
            {'actor': username, 'limit': number_of_posts})
    except Exception as e:
        return f"Error! Message: {e}"

    columns = ["URI", "Text", "Date", "User", "Likes", "Replies"]
    posts = []

    for feed in profile_feed.feed:
        posts.append([feed.post.uri, feed.post.record.text, feed.post.record.createdAt,
                      feed.post.author.handle, feed.post.likeCount, feed.post.replyCount])

    df = str(pd.DataFrame(posts, columns=columns))

    print(df)

    return df
