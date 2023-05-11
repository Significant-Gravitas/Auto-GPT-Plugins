"""Reddit Api integration using PRAW"""
import os
from typing import Any, Dict, List, Optional, Tuple, TypedDict, TypeVar

import praw
from auto_gpt_plugin_template import AutoGPTPluginTemplate

PromptGenerator = TypeVar("PromptGenerator")


class Message(TypedDict):
    role: str
    content: str


class AutoGPTReddit(AutoGPTPluginTemplate):
    """
    Reddit API integration using PRAW
    """

    def __init__(self):
        super().__init__()
        self._name = "autogpt-reddit"
        self._version = "0.1.0"
        self._description = "Reddit API integration using PRAW"
        self.client_id = os.getenv("REDDIT_CLIENT_ID")
        self.client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        self.username = os.getenv("REDDIT_USERNAME")
        self.user_agent = os.getenv("REDDIT_USER_AGENT")
        self.password = os.getenv("REDDIT_PASSWORD")

        self.api = None

        if (
                self.client_id
                and self.client_secret
                and self.username
                and self.user_agent
                and self.password
        ) is not None:
            # Authenticate to reddit
            self.api = praw.Reddit(
                client_id=self.client_id,
                client_secret=self.client_secret,
                username=self.username,
                user_agent=self.user_agent,
                password=self.password
            )
        else:
            print("Reddit credentials not found in .env file.")

    def can_handle_post_prompt(self) -> bool:
        """This method is called to check that the plugin can
        handle the post_prompt method.
        Returns:
            bool: True if the plugin can handle the post_prompt method."""
        return True

    def post_prompt(self, prompt: PromptGenerator) -> PromptGenerator:
        """This method is called just after the generate_prompt is called,
            but actually before the prompt is generated.
        Args:
            prompt (PromptGenerator): The prompt generator.
        Returns:
            PromptGenerator: The prompt generator.
        """
        if self.api:
            from .reddit import (
                get_posts_from_subreddit,
                get_comments_on_post,
                submit_post,
                submit_comment_on_post,
                reply_to_comment,
                search_reddit,
                upvote,
                downvote,
                search_reddit_user
            )

            prompt.add_command(
                "get_posts_from_subreddit",
                "Get posts from a Subreddit",
                {"subreddit": "<subreddit>", "number_of_posts": "<number_of_posts>"},
                get_posts_from_subreddit
            )
            prompt.add_command(
                "get_comments_on_post",
                "Get comments on a post",
                {"post_id": "<post_id>", "number_of_comments": "<number_of_comments>"},
                get_comments_on_post
            )
            prompt.add_command(
                "submit_post",
                "Submit a post",
                {"subreddit": "<subreddit>", "title": "<title>", "text": "<text>"},
                submit_post
            )
            prompt.add_command(
                "submit_comment_on_post",
                "Submit a comment on a post",
                {"post_id": "<post_id>", "text": "<text>"},
                submit_comment_on_post
            )
            prompt.add_command(
                "reply_to_comment",
                "Reply to a comment",
                {"comment_id": "<comment_id>", "text": "<text>"},
                reply_to_comment
            )
            prompt.add_command(
                "search_reddit",
                "Search reddit",
                {"query": "<query>", "subreddit": "<subreddit>", "number_of_posts": "<number_of_posts>"},
                search_reddit
            )
            prompt.add_command(
                "upvote",
                "Upvote a post or comment",
                {"post_id": "<post_id>", "object_type": "<object_type>"},
                upvote
            )
            prompt.add_command(
                "downvote",
                "Downvote a post or comment",
                {"post_id": "<post_id>", "object_type": "<object_type>"},
                downvote
            )
            prompt.add_command(
                "search_reddit_user",
                "Get user information",
                {"username": "<username>"},
                search_reddit_user
            )

        return prompt

    def can_handle_on_response(self) -> bool:
        """This method is called to check that the plugin can
        handle the on_response method.
        Returns:
            bool: True if the plugin can handle the on_response method."""
        return False

    def on_response(self, response: str, *args, **kwargs) -> str:
        """This method is called when a response is received from the model."""
        pass

    def can_handle_on_planning(self) -> bool:
        """This method is called to check that the plugin can
        handle the on_planning method.
        Returns:
            bool: True if the plugin can handle the on_planning method."""
        return False

    def on_planning(
            self, prompt: PromptGenerator, messages: List[str]
    ) -> Optional[str]:
        """This method is called before the planning chat completeion is done.
        Args:
            prompt (PromptGenerator): The prompt generator.
            messages (List[str]): The list of messages.
        """
        pass

    def can_handle_post_planning(self) -> bool:
        """This method is called to check that the plugin can
        handle the post_planning method.
        Returns:
            bool: True if the plugin can handle the post_planning method."""
        return False

    def post_planning(self, response: str) -> str:
        """This method is called after the planning chat completeion is done.
        Args:
            response (str): The response.
        Returns:
            str: The resulting response.
        """
        pass

    def can_handle_pre_instruction(self) -> bool:
        """This method is called to check that the plugin can
        handle the pre_instruction method.
        Returns:
            bool: True if the plugin can handle the pre_instruction method."""
        return False

    def pre_instruction(self, messages: List[str]) -> List[str]:
        """This method is called before the instruction chat is done.
        Args:
            messages (List[str]): The list of context messages.
        Returns:
            List[str]: The resulting list of messages.
        """
        pass

    def can_handle_on_instruction(self) -> bool:
        """This method is called to check that the plugin can
        handle the on_instruction method.
        Returns:
            bool: True if the plugin can handle the on_instruction method."""
        return False

    def on_instruction(self, messages: List[str]) -> Optional[str]:
        """This method is called when the instruction chat is done.
        Args:
            messages (List[str]): The list of context messages.
        Returns:
            Optional[str]: The resulting message.
        """
        pass

    def can_handle_post_instruction(self) -> bool:
        """This method is called to check that the plugin can
        handle the post_instruction method.
        Returns:
            bool: True if the plugin can handle the post_instruction method."""
        return False

    def post_instruction(self, response: str) -> str:
        """This method is called after the instruction chat is done.
        Args:
            response (str): The response.
        Returns:
            str: The resulting response.
        """
        pass

    def can_handle_pre_command(self) -> bool:
        """This method is called to check that the plugin can
        handle the pre_command method.
        Returns:
            bool: True if the plugin can handle the pre_command method."""
        return False

    def pre_command(
            self, command_name: str, arguments: Dict[str, Any]
    ) -> Tuple[str, Dict[str, Any]]:
        """This method is called before the command is executed.
        Args:
            command_name (str): The command name.
            arguments (Dict[str, Any]): The arguments.
        Returns:
            Tuple[str, Dict[str, Any]]: The command name and the arguments.
        """
        pass

    def can_handle_post_command(self) -> bool:
        """This method is called to check that the plugin can
        handle the post_command method.
        Returns:
            bool: True if the plugin can handle the post_command method."""
        return False

    def post_command(self, command_name: str, response: str) -> str:
        """This method is called after the command is executed.
        Args:
            command_name (str): The command name.
            response (str): The response.
        Returns:
            str: The resulting response.
        """
        pass

    def can_handle_chat_completion(
            self,
            messages: list[Dict[Any, Any]],
            model: str,
            temperature: float,
            max_tokens: int,
    ) -> bool:
        """This method is called to check that the plugin can
        handle the chat_completion method.
        Args:
            messages (Dict[Any, Any]): The messages.
            model (str): The model name.
            temperature (float): The temperature.
            max_tokens (int): The max tokens.
        Returns:
            bool: True if the plugin can handle the chat_completion method."""
        return False

    def handle_chat_completion(
            self,
            messages: list[Dict[Any, Any]],
            model: str,
            temperature: float,
            max_tokens: int,
    ) -> str:
        """This method is called when the chat completion is done.
        Args:
            messages (Dict[Any, Any]): The messages.
            model (str): The model name.
            temperature (float): The temperature.
            max_tokens (int): The max tokens.
        Returns:
            str: The resulting response.
        """
        return None
