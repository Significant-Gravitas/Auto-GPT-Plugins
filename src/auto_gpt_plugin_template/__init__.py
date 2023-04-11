"""This is a template for Auto-GPT plugins."""
import abc
from typing import Any, Optional

from abstract_singleton import AbstractSingleton, Singleton


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
