"""This is a template for Auto-GPT plugins."""
import abc
from typing import Any, Dict, List, Optional, Tuple, TypeVar

from abstract_singleton import AbstractSingleton, Singleton

PromptGenerator = TypeVar("PromptGenerator")


class AutoGPTPluginTemplate(AbstractSingleton, metaclass=Singleton):
    """
    This is a template for Auto-GPT plugins.
    """

    def __init__(self):
        super().__init__()
        self._name = "Auto-GPT-Plugin-Template"
        self._version = "0.1.0"
        self._description = "This is a template for Auto-GPT plugins."

    @abc.abstractmethod
    def on_response(self, response: str, *args, **kwargs) -> str:
        """This method is called when a response is received from the model."""
        pass

    @abc.abstractmethod
    def post_prompt(self, prompt: PromptGenerator) -> PromptGenerator:
        """This method is called just after the generate_prompt is called,
            but actually before the prompt is generated.

        Args:
            prompt (PromptGenerator): The prompt generator.

        Returns:
            PromptGenerator: The prompt generator.
        """
        pass

    @abc.abstractmethod
    def on_planning(
        self, prompt: PromptGenerator, messages: List[str]
    ) -> Optional[str]:
        """This method is called before the planning chat completeion is done.

        Args:
            prompt (PromptGenerator): The prompt generator.
            messages (List[str]): The list of messages.
        """
        pass

    @abc.abstractmethod
    def post_planning(self, response: str) -> str:
        """This method is called after the planning chat completeion is done.

        Args:
            response (str): The response.

        Returns:
            str: The resulting response.
        """
        pass

    @abc.abstractmethod
    def pre_instruction(self, messages: List[str]) -> List[str]:
        """This method is called before the instruction chat is done.

        Args:
            messages (List[str]): The list of context messages.

        Returns:
            List[str]: The resulting list of messages.
        """
        pass

    @abc.abstractmethod
    def on_instruction(self, messages: List[str]) -> Optional[str]:
        """This method is called when the instruction chat is done.

        Args:
            messages (List[str]): The list of context messages.

        Returns:
            Optional[str]: The resulting message.
        """
        pass

    @abc.abstractmethod
    def post_instruction(self, response: str) -> str:
        """This method is called after the instruction chat is done.

        Args:
            response (str): The response.

        Returns:
            str: The resulting response.
        """
        pass

    @abc.abstractmethod
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

    @abc.abstractmethod
    def post_command(self, command_name: str, response: str) -> str:
        """This method is called after the command is executed.

        Args:
            command_name (str): The command name.
            response (str): The response.

        Returns:
            str: The resulting response.
        """
        pass
