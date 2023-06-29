from __future__ import annotations
from typing import List, Dict

from . import AutoGPTReddit

plugin = AutoGPTReddit()


def get_posts_from_subreddit(subreddit: str, number_of_posts: int = 10) -> str:
    """Gets the top posts from a subreddit sorted by hot.

    Args:
        subreddit (str): The subreddit to get posts from.
        number_of_posts (int, optional): The number of posts to get. Default is 10.

    Returns:
        str: The list of posts.
    """

    subreddit_instance = plugin.api.subreddit(subreddit)
    top_posts = subreddit_instance.hot(limit=number_of_posts)

    posts = []

    for post in top_posts:
        post_content = post.selftext if post.is_self else post.url
        posts.append({"title": post.title, "id": post.id, "url": post.url, "content": post_content})

    return str(posts)


def get_comments_on_post(post_id: str, number_of_comments: int = 10) -> str:
    """Gets the top-level comments on a post.

    Args:
        post_id (str): The ID of the post to get the comments from.
        number_of_comments (int, optional): The number of comments to get. Default is 10.

    Returns:
        str: The list of comments containing the author, body, and comment id.
    """

    post = plugin.api.submission(id=post_id)
    post.comments.replace_more(limit=0)
    comments = []

    for comment in post.comments.list()[:number_of_comments]:
        comments.append({"author": comment.author.name, "body": comment.body, "id": comment.id})

    return str(comments)


def submit_post(subreddit: str, title: str, text: str) -> str:
    """Submits a text post to a subreddit.

    Args:
        subreddit (str): The subreddit to submit the post to.
        title (str): The title of the post.
        text (str): The text of the post.

    Returns:
        str: A string containing the success message and the title of the post and URL.
    """

    subreddit_instance = plugin.api.subreddit(subreddit)
    submission = subreddit_instance.submit(title=title, selftext=text)

    return f"Success! Post: {submission.title} URL: {submission.url}"


def submit_comment_on_post(post_id: str, text: str) -> str:
    """Submits a comment on a post.

    Args:
        post_id (str): The ID of the post to comment on.
        text (str): The text of the comment.

    Returns:
        str: A string containing the success message and the comment body.
    """
    post = plugin.api.submission(id=post_id)
    comment = post.reply(text)

    return f"Success! Comment: {comment.body}"


def reply_to_comment(comment_id: str, text: str) -> str:
    """Replies to a comment.

    Args:
        comment_id (str): The ID of the comment to reply to.
        text (str): The text of the reply.

    Returns:
        str: The author, body and ID of the reply that we posted.
    """

    comment = plugin.api.comment(id=comment_id)
    reply = comment.reply(text)
    return (
        f"author: {reply.author.name}"
        f" body: {reply.body}" 
        f" id: :{reply.id}"
    )


def search_reddit(query: str, subreddit: str = None, number_of_posts: int = 10) -> str:
    """Searches for posts based on a query. If no subreddit is specified, it will search all of Reddit.

    Args:
        query (str): The query to search for.
        subreddit (str, optional): The subreddit to search in. Default is all if nothing is specified.
        number_of_posts (int, optional): The number of posts to get. Default is 10.

    Returns:
        str: A list of posts containing the title, author, subreddit, ID and URL.
    """

    if subreddit:
        search_results = plugin.api.subreddit(subreddit).search(query, limit=number_of_posts)
    else:
        search_results = plugin.api.subreddit("all").search(query, limit=number_of_posts)

    posts = []

    for post in search_results:
        posts.append({
            "title": post.title,
            "author": post.author.name,
            "subreddit": post.subreddit.display_name,
            "id": post.id,
            "url": post.url
        })

    return str(posts)


def upvote(object_id: str, object_type) -> str:
    """Upvotes a post or comment.

    Args:
        object_id (str): The ID of the post or comment to upvote.
        object_type (str): The type of object to upvote. Either "post" or "comment".

    Returns:
        str: A string containing the success message and the ID of the post or comment upvoted.
    """

    if object_type == "post":
        obj = plugin.api.submission(id=object_id)
    elif object_type == "comment":
        obj = plugin.api.comment(id=object_id)
    else:
        return "Invalid object type, please try again with either \"post\" or \"commment\" specified."

    obj.upvote()
    return f"Upvoted {object_type} with ID: {object_id}"


def downvote(object_id: str, object_type) -> str:
    """Downvotes a post or comment.

    Args:
        object_id (str): The ID of the post or comment to downvote.
        object_type (str): The type of object to downvote. Either "post" or "comment".

    Returns:
        str: A string containing the success message and the ID of the post or comment downvoted.
    """

    if object_type == "post":
        obj = plugin.api.submission(id=object_id)
    elif object_type == "comment":
        obj = plugin.api.comment(id=object_id)
    else:
        return "Invalid object type, please try again with either \"post\" or \"commment\" specified."

    obj.downvote()
    return f"Downvoted {object_type} with ID: {object_id}"


def search_reddit_user(username: str) -> str:
    """Gets information about a Reddit user.

    Args:
        username (str): The username of the user we are querying about.

    Returns:
        Dict[str, str]: A dictionary containing information about the user.
    """

    user = plugin.api.redditor(username)
    return (
        f"name: {user.name}"
        f"id: {user.id}"
        f"comment_karma: {user.comment_karma}"
        f"link_karma: {user.link_karma}"
        f"created_utc: {user.created_utc}"
        f"recent_comments: {user.comments.new(limit=10)}"
        f"recent_submissions: {user.submissions.new(limit=10)}"
        f"is_mod: {user.is_mod}"
        f"is_gold: {user.is_gold}"
        f"is_employee: {user.is_employee}"
        f"is_friend: {user.is_friend}"
        f"is_blocked: {user.is_blocked}"
        f"is_muted: {user.is_muted}"
        f"is_contributor: {user.is_contributor}"
        f"is_subscriber: {user.is_subscriber}"
        f"has_verified_email: {user.has_verified_email}"
    )

