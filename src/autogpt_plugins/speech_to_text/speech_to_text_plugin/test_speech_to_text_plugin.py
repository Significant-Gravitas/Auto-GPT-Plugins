import unittest
from unittest.mock import patch, MagicMock
import io
import speech_to_text_plugin
from google.cloud.speech_v1p1beta1 import types

class TestSpeechToTextPlugin(unittest.TestCase):

    def test_transcribe_streaming(self):
        sample_audio = io.BytesIO(b'sample_audio_data')
        sample_transcript = "This is a sample transcript."

        with patch("speech_to_text_plugin.speech.SpeechClient") as mock_client:
            mock_instance = MagicMock()
            mock_instance.streaming_recognize.return_value = [
                types.StreamingRecognizeResponse(
                    results=[
                        types.StreamingRecognitionResult(
                            alternatives=[
                                types.SpeechRecognitionAlternative(transcript=sample_transcript)
                            ]
                        )
                    ]
                )
            ]
            mock_client.return_value = mock_instance
            transcript = speech_to_text_plugin.transcribe_streaming(sample_audio)

        self.assertEqual(transcript, sample_transcript)

    def test_process_transcribed_text(self):
        sample_transcript = "This is a sample transcript."
        sample_processed_text = "This is a sample processed text."

        with patch("speech_to_text_plugin.autogpt.process_input") as mock_process_input:
            mock_process_input.return_value = sample_processed_text
            processed_text = speech_to_text_plugin.process_transcribed_text(sample_transcript)

        self.assertEqual(processed_text, sample_processed_text)

if __name__ == '__main__':
    unittest.main()
