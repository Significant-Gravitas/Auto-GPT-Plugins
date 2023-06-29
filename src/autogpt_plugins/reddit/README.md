# ckroeper/autogpt-reddit

A plugin adding reddit API integration into Auto GPT

## Features

- Get the top posts from a subreddit using the `get_posts_from_subreddit(subreddit, number_of_posts)` command
- Get the top-level comments on a post using the `get_comments_on_post(post_id, number_of_comments)` command
- Submit a text post to a subreddit using the `submit_post(subreddit, title, text)` command
- Submit a comment on a post using the `submit_comment_on_post(post_id, text)` command
- Reply to a comment using the `reply_to_comment(comment_id, text)` command
- Search for a post based on a query using the `search_reddit(query, subreddit, number_of_posts)` command
- Upvote a post or comment using the `upvote(object_id, object_type)` command
- Downvote a post or comment using the `downvote(object_id, object_type)` command
- Get information about a reddit user using the `search_reddit_user(username)` command

## Installation

1. Clone this repo as instructed in the main repository
2. Add this chunk of code along with your reddit account information to the `.env` file within AutoGPT:

```
################################################################################
### REDDIT API
################################################################################

# Client ID && Client Secret are found on the reddit applications portal

REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=
REDDIT_USERNAME=
REDDIT_USER_AGENT=
REDDIT_PASSWORD=
```

## Reddit API Setup

1. Go to the [Reddit App Preferences](https://www.reddit.com/prefs/apps/)
2. Scroll down to the end of the "authorized applications" section and click "are you a developer? create an app..."
3. Fill out the required fields, select "script" for the app type, and provide a redirect URI (e.g., http://localhost:8080).
4. Click "Create app" button.
5. Copy the client_id (located under the app name) and client_secret (listed as "secret").
6. Update the .env file with the client_id, client_secret, and your Reddit account information.
