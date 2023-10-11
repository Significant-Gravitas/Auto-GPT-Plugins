"""This is a Chat companion plugin that turns auto-gpt into a real assisstant.
It allows you to interact with your bot via Telegram in a more natural way.
It is based on the telegram plugin I made earlier but instead of forwarding the logs to a telegram chat, it allows Auto-GPT to interact with you.

built by @wladastic on github"""

import os
import re
from typing import Any, Dict, List, Optional, Tuple, TypedDict, TypeVar

from auto_gpt_plugin_template import AutoGPTPluginTemplate

from .sophie_chat import TelegramUtils

PromptGenerator = TypeVar("PromptGenerator")

class Message(TypedDict):
    role: str
    content: str


def remove_color_codes(s: str) -> str:
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", s)


class SophieTelegram(AutoGPTPluginTemplate):
    """
    This is a companion plugin for Auto-GPT that allows you to interact with your bot via Telegram in a more natural way.
    """

    def __init__(self):
        super().__init__()
        self._name = "Auto-GPT-Sophie"
        self._version = "0.3.0"
        self._description = (
            "This integrates a Telegram chat bot with your autogpt instance."
        )
        self.telegram_sophie_api_key = os.getenv("TELEGRAM_SOPHIE_API_KEY", None)
        self.telegram_sophie_chat_id = os.getenv("TELEGRAM_SOPHIE_CHAT_ID", None)
        self.telegram_sophie_utils = TelegramUtils(
            chat_id=self.telegram_sophie_chat_id,
            api_key=self.telegram_sophie_api_key
        )

    def post_prompt(self, prompt: PromptGenerator) -> PromptGenerator:
        """This method is called just after the generate_prompt is called,
        but actually before the prompt is generated.
        Args:
            prompt (PromptGenerator): The prompt generator.
        Returns:
            PromptGenerator: The prompt generator.
        """

        prompt.add_command(
            "get_previous_message_history",
            "Get the previous messages from the chat when you start.",
            {},
            self.telegram_sophie_utils.get_previous_message_history,
        )

        prompt.add_command(
            "ask_user",
            "Ask the user for input or tell them something and wait for their response if.",
            {
                "prompt": "string",
            },
            self.telegram_sophie_utils.ask_user,
        )

        prompt.add_command(
            "ask_user_voice",
            "Same as ask_user but also sends a friendly voice message.",
            {
                "prompt": "string",
            },
            self.telegram_sophie_utils.ask_user_voice,
        )

        prompt.add_command(
            "send_message",
            "Send a message to the user without awaiting response.",
            {
                "message": "string",
            },
            self.telegram_sophie_utils.send_message,
        )

        prompt.add_command(
            "send_voice_message",
            "Same as send_message but also sends a friendly voice message.",
            {
                "message": "string",
            },
            self.telegram_sophie_utils.send_message_and_speak,
        )

        prompt.add_command(
            "sleep_until_interaction",
            "To be used to pause the conversation for next user interaction. Similar to ask but without a prompt, user is only notified that you sleep.",
            {},
            self.telegram_sophie_utils.idle_until_interaction,
        )

        return prompt

    def can_handle_post_prompt(self) -> bool:
        """This method is called to check that the plugin can
        handle the post_prompt method.
        Returns:
            bool: True if the plugin can handle the post_prompt method."""
        return True

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
            self, prompt: PromptGenerator, messages: List[Message]
    ) -> Optional[str]:
        """This method is called before the planning chat completion is done.
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
        """This method is called after the planning chat completion is done.
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

    def pre_instruction(self, messages: List[Message]) -> List[Message]:
        """This method is called before the instruction chat is done.
        Args:
            messages (List[Message]): The list of context messages.
        Returns:
            List[Message]: The resulting list of messages.
        """
        pass

    def can_handle_on_instruction(self) -> bool:
        """This method is called to check that the plugin can
        handle the on_instruction method.
        Returns:
            bool: True if the plugin can handle the on_instruction method."""
        return False

    def on_instruction(self, messages: List[Message]) -> Optional[str]:
        """This method is called when the instruction chat is done.
        Args:
            messages (List[Message]): The list of context messages.
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
            self, messages: Dict[Any, Any], model: str, temperature: float, max_tokens: int
    ) -> bool:
        """This method is called to check that the plugin can
          handle the chat_completion method.
        Args:
            messages (List[Message]): The messages.
            model (str): The model name.
            temperature (float): The temperature.
            max_tokens (int): The max tokens.
          Returns:
              bool: True if the plugin can handle the chat_completion method."""
        return False

    def handle_chat_completion(
            self, messages: List[Message], model: str, temperature: float, max_tokens: int
    ) -> str:
        """This method is called when the chat completion is done.
        Args:
            messages (List[Message]): The messages.
            model (str): The model name.
            temperature (float): The temperature.
            max_tokens (int): The max tokens.
        Returns:
            str: The resulting response.
        """
        pass

    def can_handle_text_embedding(
        self, text: str
    ) -> bool:
        return False
    
    def handle_text_embedding(
        self, text: str
    ) -> list:
        pass
    
    def can_handle_user_input(self, user_input: str) -> bool:
        return False

    def user_input(self, user_input: str) -> str:
        return user_input

    def can_handle_report(self) -> bool:
        return False

    def report(self, message: str) -> None:
        pass