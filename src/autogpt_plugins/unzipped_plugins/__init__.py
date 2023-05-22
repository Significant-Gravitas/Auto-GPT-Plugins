"""
This plugin allows developers to use unzipped plugins simplifying
the plugin development process.
"""
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, TypeVar, TypedDict
from auto_gpt_plugin_template import AutoGPTPluginTemplate
from .plugin_manager import PluginManager

PromptGenerator = TypeVar("PromptGenerator")


class Message(TypedDict):
    """Message type for the on_response method."""

    role: str
    content: str


class AutoGPTAllowUnzippedPlugins(AutoGPTPluginTemplate):
    """
    This plugin allows developers to use unzipped plugins simplifying
    the plugin development process.
    """

    def __init__(self, plugin_manager: PluginManager = None):
        super().__init__()
        self._name = "Auto-GPT-Allow-Unzipped-Plugins"
        self._version = "0.2.0"
        self._description = (
            "This plugin allows developers to use "
            "unzipped plugins simplifying the plugin"
            "development process."
        )

        # Walk up the directory tree till you find a folder called "plugins"
        plugins_dir = Path(__file__).parent
        while plugins_dir.name != "plugins" and plugins_dir.parent != plugins_dir:
            plugins_dir = plugins_dir.parent

        if plugin_manager is None:
            plugin_manager = PluginManager

        if plugins_dir.name != "plugins":
            raise FileNotFoundError("Could not find plugins directory.")

        if os.getenv("UNZIPPED_PLUGIN_INSTALL_REQUIREMENTS", "True") == "True":
            plugin_manager.install_plugin_requirements(plugins_dir)
        self._plugins = plugin_manager.load_unzipped_plugins(plugins_dir)

    def _can_handle(self, method) -> bool:
        can_handle_method = f"can_handle_{method}"
        return any(
            hasattr(plugin, can_handle_method) and getattr(plugin, can_handle_method)()
            for plugin in self._plugins
        )

    def can_handle_on_response(self) -> bool:
        return self._can_handle("on_response")

    def on_response(self, response: str, *args, **kwargs) -> str:
        for plugin in self._plugins:
            if not plugin.can_handle_on_response():
                continue
            response = plugin.on_response(response, *args, **kwargs)
        return response

    def can_handle_post_prompt(self) -> bool:
        return self._can_handle("post_prompt")

    def post_prompt(self, prompt: PromptGenerator) -> PromptGenerator:
        for plugin in self._plugins:
            if not plugin.can_handle_post_prompt():
                continue
            prompt = plugin.post_prompt(prompt)
        return prompt

    def can_handle_on_planning(self) -> bool:
        """On Planning is not supported by this plugin."""
        return False

    def on_planning(
        self, prompt: PromptGenerator, messages: List[Message]
    ) -> Optional[str]:
        pass

    def can_handle_post_planning(self) -> bool:
        return self._can_handle("post_planning")

    def post_planning(self, response: str) -> str:
        for plugin in self._plugins:
            if not plugin.can_handle_post_planning():
                continue
            response = plugin.post_planning(response)
        return response

    def can_handle_pre_instruction(self) -> bool:
        return self._can_handle("pre_instruction")

    def pre_instruction(self, messages: List[Message]) -> List[Message]:
        for plugin in self._plugins:
            if not plugin.can_handle_pre_instruction():
                continue
            if plugin_messages := plugin.pre_instruction(messages):
                messages.extend(iter(plugin_messages))
        return messages

    def can_handle_on_instruction(self) -> bool:
        return self._can_handle("on_instruction")

    def on_instruction(self, messages: List[Message]) -> Optional[str]:
        plugins_reply = ""
        for i, plugin in enumerate(self._plugins):
            if not plugin.can_handle_on_instruction():
                continue
            if plugin_result := plugin.on_instruction(messages):
                sep = "\n" if i else ""
                plugins_reply = f"{plugins_reply}{sep}{plugin_result}"
        return plugins_reply

    def can_handle_post_instruction(self) -> bool:
        return self._can_handle("post_instruction")

    def post_instruction(self, response: str) -> str:
        for plugin in self._plugins:
            if not plugin.can_handle_post_instruction():
                continue
            response = plugin.post_instruction(response)
        return response

    def can_handle_pre_command(self) -> bool:
        return self._can_handle("pre_command")

    def pre_command(
        self, command_name: str, arguments: Dict[str, Any]
    ) -> Tuple[str, Dict[str, Any]]:
        for plugin in self._plugins:
            if not plugin.can_handle_pre_command():
                continue
            command_name, arguments = plugin.pre_command(command_name, arguments)
        return command_name, arguments

    def can_handle_post_command(self) -> bool:
        return self._can_handle("post_command")

    def post_command(self, command_name: str, response: str) -> str:
        for plugin in self._plugins:
            if not plugin.can_handle_post_command():
                continue
            response = plugin.post_command(command_name, response)
        return response

    def can_handle_chat_completion(
        self, messages: Dict[Any, Any], model: str, temperature: float, max_tokens: int
    ) -> bool:
        """Not supported by this plugin."""
        return False

    def handle_chat_completion(
        self, messages: List[Message], model: str, temperature: float, max_tokens: int
    ) -> str:
        pass

    def can_handle_text_embedding(self, text: str) -> bool:  # type: ignore
        """Not yet supported by this plugin"""
        return False

    def handle_text_embedding(self, text: str) -> list:  # type: ignore
        """Not yet supported by this plugin"""

    def can_handle_user_input(self, user_input: str) -> bool:
        """Check if the plugin can handle user input."""
        return any(
            hasattr(plugin, "can_handle_user_input")
            and plugin.can_handle_user_input(user_input=user_input)
            for plugin in self._plugins
        )

    def user_input(self, user_input: str) -> str:
        """
        Handles user input.
        """
        for plugin in self._plugins:
            if not hasattr(plugin, "can_handle_user_input"):
                continue
            if not plugin.can_handle_user_input(user_input=user_input):
                continue
            plugin_response = plugin.user_input(user_input=user_input)
            if not plugin_response:
                continue
            else:
                return plugin_response
        return None

    def can_handle_report(self) -> bool:
        """Checks if the plugin can handle reporting."""
        return self._can_handle("report")

    def report(self, message: str) -> None:
        """Handles reporting."""
        for plugin in self._plugins:
            if not hasattr(plugin, "can_handle_report"):
                continue
            if not plugin.can_handle_report():
                continue
            plugin.report(message)
