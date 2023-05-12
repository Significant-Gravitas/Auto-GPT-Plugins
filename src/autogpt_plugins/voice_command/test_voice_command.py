import os
import unittest

from .voice_command_kaldi import VoiceCommandKaldi


class TestVoiceCommand(unittest.TestCase):
    # voice command Tests

    def setUp(self):
        os.environ["VOICE_COMMAND_ENABLE"] = "True"
        os.environ["VOICE_COMMAND_SDK"] = "kaldi"
        self.plugin = VoiceCommandKaldi()

    def tearDown(self):
        os.environ.pop("VOICE_COMMAND_ENABLE", None)
        os.environ.pop("VOICE_COMMAND_SDK", None)

    def test_init_model(self):
        try:
            self.plugin.init_model()
        except Exception as e:
            self.assertEqual(e, 'MODEL_INIT_ERROR')
