import json
import os
import pytest

from unittest.mock import MagicMock, patch, mock_open

from .voice_command_kaldi import VoiceCommandKaldi


class KaldiRecognizerMockup:

    def __init__(self):
        pass

    def Result(self):
        return json.dumps({
            "text": "hello"
        })


def mock_record_cb():
    pass


def mock_speech():
    pass


class TestVoiceCommand:
    # voice command Tests

    @pytest.fixture(autouse=True)
    def setUp(self):

        os.environ["VOICE_COMMAND_ENABLE"] = "True"
        os.environ["VOICE_COMMAND_SDK"] = "kaldi"
        # os.environ["VOICE_COMMAND_INITCALL"] = "hello"
        # os.environ["VOICE_COMMAND_CONFIRM"] = "False"
        self.plugin = VoiceCommandKaldi()

    @pytest.fixture(autouse=True)
    def tearDown(self):
        os.environ.pop("VOICE_COMMAND_ENABLE", None)
        os.environ.pop("VOICE_COMMAND_SDK", None)
        os.environ.pop("VOICE_COMMAND_INITCALL", None)
        os.environ.pop("VOICE_COMMAND_CONFIRM", None)

    def test_init_model(self):
        try:
            self.plugin.init_model()
        except Exception as e:
            assert e == 'MODEL_INIT_ERROR'

    def test_initcall_default(self):
        assert self.plugin.initiator == 'hello'

    def test_initcall_user_defined(self):
        os.environ["VOICE_COMMAND_INITCALL"] = "hi"
        plugin2 = VoiceCommandKaldi()
        assert plugin2.initiator == 'hi'

    def test_confirmation_default(self):
        assert self.plugin.confirmation is False

    def test_confirmation_user_defined(self):
        os.environ["VOICE_COMMAND_CONFIRM"] = "True"
        plugin2 = VoiceCommandKaldi()
        assert plugin2.confirmation is True

    def test_when_recognizer_is_none(self):
        plugin3 = VoiceCommandKaldi()
        self.recognizer = None
        resp = plugin3.run(is_test=True)
        assert resp == "Module initialization error"

    def test_fill_queue(self):
        self.plugin._record_cb("test_data".encode(), None, None, None)
        assert self.plugin.q.empty() is False

    @patch('requests.get')
    def test_speech_is_true(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = None
        mock_requests.return_value = mock_response
        resp = self.plugin._speech("test 1 2 3")
        assert resp is True

    # def test_speech_play_sound(self):
    #     resp = self.plugin._speech("test 1 2 3")
    #     assert resp is True

    @patch('requests.get')
    def test_speech_is_false(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_requests.return_value = mock_response
        resp = self.plugin._speech("test 1 2 3")
        assert resp is False

    def test_get_state1(self):

        self.plugin.recognizer = MagicMock(return_value=KaldiRecognizerMockup)
        self.plugin.recognizer.AcceptWaveform = MagicMock(return_value=True)
        self.plugin.q = MagicMock(return_value=bytes('testing'.encode()))
        self.plugin._speech = MagicMock(return_value=mock_speech)
        self.plugin._record_cb = MagicMock(return_value=mock_record_cb)
        self.plugin.recognizer.Result = MagicMock(return_value=json.dumps({"text": "hello"}))

        m = mock_open()
        with patch('sounddevice.RawInputStream', m, create=True):
            resp = self.plugin.run(is_test=True)
        assert resp == "yes sir"

    def test_get_state2_no(self):
        self.plugin.recognizer = MagicMock(return_value=KaldiRecognizerMockup)
        self.plugin.recognizer.AcceptWaveform = MagicMock(return_value=True)
        self.plugin.q = MagicMock(return_value=bytes('testing'.encode()))
        self.plugin._speech = MagicMock(return_value=mock_speech)
        self.plugin._record_cb = MagicMock(return_value=mock_record_cb)
        self.plugin.recognizer.Result = MagicMock(return_value=json.dumps({"text": "no"}))

        m = mock_open()
        with patch('sounddevice.RawInputStream', m, create=True):
            resp = self.plugin.run(is_test=True, force_state=2)
        assert resp == "n"

    def test_get_state2_yes(self):
        self.plugin.recognizer = MagicMock(return_value=KaldiRecognizerMockup)
        self.plugin.recognizer.AcceptWaveform = MagicMock(return_value=True)
        self.plugin.q = MagicMock(return_value=bytes('testing'.encode()))
        self.plugin._speech = MagicMock(return_value=mock_speech)
        self.plugin._record_cb = MagicMock(return_value=mock_record_cb)
        self.plugin.recognizer.Result = MagicMock(return_value=json.dumps({"text": "yes"}))

        m = mock_open()
        with patch('sounddevice.RawInputStream', m, create=True):
            resp = self.plugin.run(is_test=True, force_state=2)
        assert resp == "y"

    def test_get_state2_query_without_confirmation(self):
        self.plugin.recognizer = MagicMock(return_value=KaldiRecognizerMockup)
        self.plugin.recognizer.AcceptWaveform = MagicMock(return_value=True)
        self.plugin.q = MagicMock(return_value=bytes('testing'.encode()))
        self.plugin._speech = MagicMock(return_value=mock_speech)
        self.plugin._record_cb = MagicMock(return_value=mock_record_cb)
        self.plugin.recognizer.Result = MagicMock(return_value=json.dumps({"text": "call me"}))
        self.plugin.confirmation = False

        m = mock_open()
        with patch('sounddevice.RawInputStream', m, create=True):
            resp = self.plugin.run(is_test=True, force_state=2)
        assert resp == "call me"

    def test_get_state2_query_with_confirmation(self):
        self.plugin.recognizer = MagicMock(return_value=KaldiRecognizerMockup)
        self.plugin.recognizer.AcceptWaveform = MagicMock(return_value=True)
        self.plugin.q = MagicMock(return_value=bytes('testing'.encode()))
        self.plugin._speech = MagicMock(return_value=mock_speech)
        self.plugin._record_cb = MagicMock(return_value=mock_record_cb)
        self.plugin.recognizer.Result = MagicMock(return_value=json.dumps({"text": "call me"}))
        self.plugin.confirmation = True

        m = mock_open()
        with patch('sounddevice.RawInputStream', m, create=True):
            resp = self.plugin.run(is_test=True, force_state=2)
        assert resp == "Did you say call me ? yes or no"

    def test_get_state3_no(self):
        self.plugin.recognizer = MagicMock(return_value=KaldiRecognizerMockup)
        self.plugin.recognizer.AcceptWaveform = MagicMock(return_value=True)
        self.plugin.q = MagicMock(return_value=bytes('testing'.encode()))
        self.plugin._speech = MagicMock(return_value=mock_speech)
        self.plugin._record_cb = MagicMock(return_value=mock_record_cb)
        self.plugin.recognizer.Result = MagicMock(return_value=json.dumps({"text": "no"}))
        self.plugin.confirmation = True

        m = mock_open()
        with patch('sounddevice.RawInputStream', m, create=True):
            resp = self.plugin.run(is_test=True, force_state=3)
        assert resp == "Please repeat again"

    def test_get_state3_yes(self):
        self.plugin.recognizer = MagicMock(return_value=KaldiRecognizerMockup)
        self.plugin.recognizer.AcceptWaveform = MagicMock(return_value=True)
        self.plugin.q = MagicMock(return_value=bytes('testing'.encode()))
        self.plugin._speech = MagicMock(return_value=mock_speech)
        self.plugin._record_cb = MagicMock(return_value=mock_record_cb)
        self.plugin.recognizer.Result = MagicMock(return_value=json.dumps({"text": "yes"}))
        self.plugin.confirmation = True

        m = mock_open()
        with patch('sounddevice.RawInputStream', m, create=True):
            resp = self.plugin.run(is_test=True, force_state=3)
        assert resp == "testing"
