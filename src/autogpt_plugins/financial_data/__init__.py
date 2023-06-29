"""This is the plugin for generating company financial data for Auto-GPT."""
import os
from typing import Any, Dict, List, Optional, Tuple, TypedDict, TypeVar
from auto_gpt_plugin_template import AutoGPTPluginTemplate
from .financial_analysis import generate_financial_data

PromptGenerator = TypeVar("PromptGenerator")


class Message(TypedDict):
    role: str
    content: str


class AutoGPTFinancialAnalysis(AutoGPTPluginTemplate):
    def __init__(self):
        super().__init__()
        self._name = "Financial-Analysis"
        self._version = "0.1.0"
        self.needAnalyse = False
        self.symbol = ""
        self._description = (
            "Generate Company Financial Data for Analysis Plugin for Auto-GPT. "
        )

    def can_handle_post_prompt(self) -> bool:
        return True

    def post_prompt(self, prompt: PromptGenerator) -> PromptGenerator:
        prompt.add_command(
                "Generate Financial Data",
                "generate_financial_data",
                {"symbol": "<symbol>"},
                generate_financial_data,
            )
        return prompt

    def can_handle_pre_command(self) -> bool:
        return True

    def pre_command(
        self, command_name: str, arguments: Dict[str, Any]
    ) -> Tuple[str, Dict[str, Any]]:
        if command_name == "generate_financial_data":
            symbol = arguments["symbol"]
            prompt = generate_financial_data(symbol)
            # getcwd + auto_gpt_workspace
            filename = os.getcwd() + f"/autogpt/auto_gpt_workspace/financial_analysis_{symbol}.txt"
            print(filename)
            return "write_to_file", {"filename": filename, "text": prompt}
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

    def can_handle_chat_completion(
        self, messages: Dict[Any, Any], model: str, temperature: float, max_tokens: int
    ) -> bool:
        return False

    def handle_chat_completion(
        self, messages: List[Message], model: str, temperature: float, max_tokens: int
    ) -> str:
        pass
