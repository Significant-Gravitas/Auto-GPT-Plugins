# test_speech_to_text_plugin.py

import unittest
from unittest.mock import patch, MagicMock
import io
import pyaudio
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

    @patch("speech_to_text_plugin.pyaudio.PyAudio")
    def test_record_audio(self, mock_pyaudio):
        # Mock the PyAudio's open method to return a stream that yields mock audio data
        mock_pyaudio().open().read.return_value = b"mock audio data"

        # Get a generator from the record_audio function
        audio_data_generator = speech_to_text_plugin.record_audio()

        # Verify the generator yields the expected audio data
        self.assertEqual(next(audio_data_generator), b"mock audio data")

if __name__ == '__main__':
    unittest.main()
