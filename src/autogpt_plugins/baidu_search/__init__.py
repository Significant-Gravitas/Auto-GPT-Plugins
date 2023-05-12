"""This is the Baidu search engines plugin for Auto-GPT."""
import os
from typing import Any, Dict, List, Optional, Tuple, TypedDict, TypeVar
from auto_gpt_plugin_template import AutoGPTPluginTemplate
from .baidu_search import _baidu_search

PromptGenerator = TypeVar("PromptGenerator")


class Message(TypedDict):
    role: str
    content: str


class AutoGPTBaiduSearch(AutoGPTPluginTemplate):
    def __init__(self):
        super().__init__()
        self._name = "Baidu-Search-Plugin"
        self._version = "0.1.0"
        self._description = (
            "This plugin performs Baidu searches using the provided query."
        )
        self.load_commands = (
            os.getenv("SEARCH_ENGINE")
            and os.getenv("SEARCH_ENGINE").lower() == "baidu"
            and os.getenv("BAIDU_COOKIE")
        )

    def can_handle_post_prompt(self) -> bool:
        return True

    def post_prompt(self, prompt: PromptGenerator) -> PromptGenerator:
        if self.load_commands:
            # Add Baidu Search command
            prompt.add_command(
                "Baidu Search",
                "baidu_search",
                {"query": "<query>"},
                _baidu_search,
            )
        else:
            print(
                "Warning: Baidu-Search-Plugin is not fully functional. "
                "Please set the SEARCH_ENGINE and BAIDU_COOKIE environment variables."
            )
        return prompt

    def can_handle_pre_command(self) -> bool:
        return True

    def pre_command(
        self, command_name: str, arguments: Dict[str, Any]
    ) -> Tuple[str, Dict[str, Any]]:
        if command_name == "google" and self.load_commands:
            return "baidu_search", {"query": arguments["query"]}
        else:
            return command_name, arguments

    def can_handle_post_command(self) -> bool:
        return False

    def post_command(self, command_name: str, response: str) -> str:
        pass

    def can_handle_on_planning(self) -> bool:
        return False

    def on_planning(
        self, prompt: PromptGenerator, messages: List[Message]
    ) -> Optional[str]:
        pass

    def can_handle_on_response(self) -> bool:
        return False

    def on_response(self, response: str, *args, **kwargs) -> str:
        pass

    def can_handle_post_planning(self) -> bool:
        return False

    def post_planning(self, response: str) -> str:
        pass

    def can_handle_pre_instruction(self) -> bool:
        return False

    def pre_instruction(self, messages: List[Message]) -> List[Message]:
        pass

    def can_handle_on_instruction(self) -> bool:
        return False

    def on_instruction(self, messages: List[Message]) -> Optional[str]:
        pass

    def can_handle_post_instruction(self) -> bool:
        return False

    def post_instruction(self, response: str) -> str:
        pass

    def can_handle_pre_command(self) -> bool:
        return True

    def can_handle_chat_completion(
        self, messages: Dict[Any, Any], model: str, temperature: float, max_tokens: int
    ) -> bool:
        return False

    def handle_chat_completion(
        self, messages: List[Message], model: str, temperature: float, max_tokens: int
    ) -> str:
        pass
