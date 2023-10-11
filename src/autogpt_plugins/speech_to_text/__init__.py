from typing import Any, Dict, List, Optional, Tuple, TypedDict, TypeVar

from auto_gpt_plugin_template import AutoGPTPluginTemplate
from .speech_to_text_plugin import transcribe_audio

PromptGenerator = TypeVar("PromptGenerator")

class SpeechToTextPlugin(AutoGPTPluginTemplate):
    """
    This is the Auto-GPT Speech-to-Text plugin.
    """

    def __init__(self):
        super().__init__()
        self._name = "Auto-GPT-Speech-to-Text-Plugin"
        self._version = "0.0.1"
        self._description = "Auto-GPT Speech-to-Text Plugin: Transcribe spoken input in real-time."

    def can_handle_post_prompt(self) -> bool:
        return True

    def post_prompt(self, prompt: PromptGenerator) -> PromptGenerator:
        prompt.add_command(
            "Transcribe spoken input",
            "transcribe_audio",
            {
                "audio": "<audio>",
            },
            transcribe_audio,
        )
        return prompt

    # Add more methods as needed, such as can_handle_on_response, on_response, etc.

