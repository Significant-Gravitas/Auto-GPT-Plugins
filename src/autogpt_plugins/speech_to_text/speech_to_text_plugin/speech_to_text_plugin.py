from typing import Any, Dict, List, Optional, Tuple, TypedDict, TypeVar

from auto_gpt_plugin_template import AutoGPTPluginTemplate
from .speech_to_text_plugin import transcribe_streaming, record_audio, process_transcribed_text
import io

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
        # Record audio from the built-in microphone
        audio_data = next(record_audio())

        # Transcribe the audio data using Google Speech-to-Text
        transcript = transcribe_streaming(io.BytesIO(audio_data))
        if transcript:
            # Process the transcribed text
            processed_text = process_transcribed_text(transcript)

            # Add the processed text to the prompt
            prompt.add_text(processed_text)

        return prompt
