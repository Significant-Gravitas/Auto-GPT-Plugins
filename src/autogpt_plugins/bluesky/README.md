# Auto-GPT Bluesky Plugin

A plugin that adds Bluesky API integration into Auto GPT

## Features (more coming soon!)

- Post a message using the `post_to_bluesky(text)` command
- Get recent posts using the `get_bluesky_posts(username, number_of_posts)` command

## Installation

1. Clone this repo as instructed in the main repository
2. Add this chunk of code along with your Bluesky Username and App Password information to the `.env` file within AutoGPT:

```
################################################################################
### BLUESKY API
################################################################################

# Create an App Password here: Bluesky -> Settings -> Advanced -> App Passwords

BLUESKY_USERNAME=
BLUESKY_APP_PASSWORD=
```