# AutoGPT Chat With User Plugin

This plugin gives ChatGPT a command to chat with the user during the command cycle. In cases where the agent wishes to chat with the user, the desire to chat frequently comes as a quasi-hallucination where the agent thinks it is talking, but it isn't. Agents also tend to think that simple agents can talk with the user (they can't). This command gives the agent an option ot use a cycle to talk with the user as a discrete action.

## Key Features:
- Launches an environment-agnostic simple chat window.
- Chat messages are passed in to the window. When user replies, message is passed back to agent as-if it had just executed a non-interactive command.

## Installation:
As part of the AutoGPT plugins package, follow the [installation instructions](https://github.com/Significant-Gravitas/Auto-GPT-Plugins) on the Auto-GPT-Plugins GitHub reporistory README page.

## AutoGPT Configuration

Set `ALLOWLISTED_PLUGINS=AutoGPTChatWithUser,example-plugin1,example-plugin2,etc` in your AutoGPT `.env` file.
