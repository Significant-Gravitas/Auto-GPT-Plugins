import os
from unittest.mock import patch, MagicMock
import unittest
import gradio_tools
from .tools import (AutoGPTClipInterrogatorTool,
                    AutoGPTStableDiffusion,
                    AutoGPTWhisperTool,
                    AutoGPTTextToVideoTool,
                    AutoGPTCaptioner,
                    AutoGPTPromptGeneratorTool,
                    AutoGPTImageToMusicTool,
                    AutoGPTDocumentAnsweringTool)


class TestGradioTools(unittest.TestCase):
    @patch.dict(
        os.environ,
        {
            "AUTOGPT_GRADIO_TOOLS": "WhisperAudioTranscription,TextToVideo",
        },
    )
    def test_right_tools_loaded(self):
        from . import AutoGPTGradioTools

        plugin = AutoGPTGradioTools()
        assert plugin.tools[0].name == "WhisperAudioTranscription"
        assert plugin.tools[1].name == "TextToVideo"

    @patch.dict(
        os.environ,
        {
            "AUTOGPT_GRADIO_TOOLS": "WhisperAudioTranscription,TextToVideo",
        },
    )
    def test_commands_added_to_prompt(self):
        from . import AutoGPTGradioTools

        mock_prompt = MagicMock()
        plugin = AutoGPTGradioTools()
        plugin.post_prompt(mock_prompt)
        # Two tools added to prompt
        assert mock_prompt.add_command.call_count == 2
    

    def test_tools_configured_correctly(self):
        all_tools = [
            (AutoGPTClipInterrogatorTool(), gradio_tools.ClipInterrogatorTool()),
            (AutoGPTStableDiffusion(), gradio_tools.StableDiffusionTool()),
            (AutoGPTWhisperTool(), gradio_tools.WhisperAudioTranscriptionTool()),
            (AutoGPTTextToVideoTool(), gradio_tools.TextToVideoTool()),
            (AutoGPTCaptioner(), gradio_tools.ImageCaptioningTool()),
            (AutoGPTPromptGeneratorTool(), gradio_tools.StableDiffusionPromptGeneratorTool()),
            (AutoGPTImageToMusicTool(), gradio_tools.ImageToMusicTool()),
            (AutoGPTDocumentAnsweringTool(), gradio_tools.DocQueryDocumentAnsweringTool())
        ]
        for tool_1, tool_2 in all_tools:
            assert tool_1.name == tool_2.name
            assert tool_1.description == tool_2.description
            assert tool_1.src == tool_2.src
            assert tool_1.args
