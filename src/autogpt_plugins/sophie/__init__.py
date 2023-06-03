"""This is a Chat companion plugin that turns auto-gpt into a real assisstant.
It allows you to interact with your bot via Telegram in a more natural way.
It is based on the telegram plugin I made earlier but instead of forwarding the logs to a telegram chat, it allows Auto-GPT to interact with you.

built by @wladastic on github"""

from typing import Any, Dict, List, Optional, Tuple, TypedDict, TypeVar
import os
import re

from auto_gpt_plugin_template import AutoGPTPluginTemplate

PromptGenerator = TypeVar("PromptGenerator")
from .sophie_chat import TelegramUtils


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
        self._name = "AutoGPT-Sophie-Plugin"
        self._name = "Auto-GPT-Sophie"
        self._version = "0.2.0"
        self._description = (
            "This integrates a Telegram chat bot with your autogpt instance."
        )
        self.telegram_api_key = os.getenv("TELEGRAM_SOPHIE_API_KEY", None)
        self.telegram_chat_id = os.getenv("TELEGRAM_SOPHIE_CHAT_ID", None)
        self.telegram_utils = TelegramUtils(
            chat_id=self.telegram_chat_id, api_key=self.telegram_api_key
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
            "ask_user",
            "Ask the user for input or tell them something and wait for their response.",
            {
                "prompt": "<message that awaits user input>",
            },
            self.telegram_utils.ask_user,
        )

        prompt.add_command(
            "ask_user_voice",
            "Ask the user for input or tell them something and wait for their response.",
            {
                "prompt": "<message that awaits user input>",
            },
            self.telegram_utils.ask_user_voice,
        )

        prompt.add_command(
            "send_message",
            "Send a message to the user without awaiting response.",
            {
                "message": "<message to send>",
            },
            self.telegram_utils.send_message,
        )

        prompt.add_command(
            "send_voice_message",
            "Send a message to the user without awaiting response.",
            {
                "message": "<message to send>",
            },
            self.telegram_utils.send_message_and_speak,
        )

        prompt.add_command(
            "sleep_until_interaction",
            "Wait until the user sends a message, for example after saying good night.",
            {},
            self.telegram_utils.idle_until_interaction,
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
        return True

    def post_planning(self, response: str) -> str:
        """This method is called after the planning chat completion is done.
        Args:
            response (str): The response.
        Returns:
            str: The resulting response.
        """
        try:
            assistant_thoughts = response.get("thoughts", {})
            assistant_thoughts_speak = assistant_thoughts.get("speak")
            # self.telegram_utils.send_message_and_speak(assistant_thoughts_speak)
        except Exception as e:
            print(e)
            print("Could not send assistant thoughts to telegram.")
        return response

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

    def can_handle_user_input(self, user_input: str) -> bool:
        """This method is called to check that the plugin can
        handle the user_input method.

        Args:
            user_input (str): The user input.

        Returns:
            bool: True if the plugin can handle the user_input method."""
        return False

    def user_input(self, user_input: str) -> str:
        user_input = remove_color_codes(user_input)
        # if the user_input is too long, shorten it

        return self.telegram_utils.ask_user(prompt=user_input)

    def can_handle_report(self) -> bool:
        """This method is called to check that the plugin can
        handle the report method.

        Returns:
            bool: True if the plugin can handle the report method."""
        return False

    def report(self, message: str) -> None:
        pass

    def can_handle_text_embedding(self, text: str) -> bool:
        """This method is called to check that the plugin can
          handle the text_embedding method.
        Args:
            text (str): The text to be convert to embedding.
          Returns:
              bool: True if the plugin can handle the text_embedding method."""
        return False

    def handle_text_embedding(self, text: str) -> list:
        """This method is called when the chat completion is done.
        Args:
            text (str): The text to be convert to embedding.
        Returns:
            list: The text embedding.
        """
        pass