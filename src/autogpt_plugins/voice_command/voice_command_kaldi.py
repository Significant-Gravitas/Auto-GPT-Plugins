import os
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from playsound import playsound
import json
import requests


class VoiceCommandKaldi:

    def __init__(self):
        super().__init__()

        self.recognizer = None
        self.model = None
        self.initiator = 'hello'
        self.confirmation = False

        if os.getenv("VOICE_COMMAND_INITCALL") is not None:
            self.initiator = os.getenv("VOICE_COMMAND_INITCALL")

        if os.getenv("VOICE_COMMAND_CONFIRM") is not None and os.getenv("VOICE_COMMAND_CONFIRM") == "True":
            self.confirmation = True

        self.q = queue.Queue()

        self.init_model()

    def init_model(self):
        try:
            print("Display input/output devices")
            print(sd.query_devices())
            print(sd.default.device[0])

            device_info = sd.query_devices(sd.default.device[0], 'input')
            samplerate = int(device_info['default_samplerate'])

            self.model = Model(r"./model")
            self.recognizer = KaldiRecognizer(self.model, samplerate)
            self.recognizer.SetWords(False)

        except Exception as e:
            self.recognizer = None
            print('MODEL_INIT_ERROR')

    def run(self, is_test=False, force_state=None) -> str:

        if self.recognizer is None:
            print("Please reinitialize the module again")
            return "Module initialization error"

        print("==> Begin recording. Press Ctrl+C to stop the recording ")
        try:
            with sd.RawInputStream(dtype='int16', channels=1, callback=self._record_cb):

                command_query = 'None'

                # state 1 : wait for init call
                # state 2 : wait for question
                # state 3 : wait for confirmation

                state = 1
                if force_state:
                    state = force_state

                while True:
                    data = self.q.get()

                    if self.recognizer.AcceptWaveform(data):

                        text = self._get_result().get("text", "")

                        # state 1 : wait for init call
                        if state == 1 and self.initiator in text:
                            speech_txt = "yes sir"
                            print("[System Voice] " + speech_txt)
                            self._speech(speech_txt)
                            state = 2
                            if is_test:
                                return speech_txt
                            continue

                        # state 2 : wait for question
                        if state == 2 and not text == "" and "yes sir" not in text:
                            command_query = text
                            # Handle simple 'yes/no' answer and return character 'y/n'
                            if text == "no":
                                command_query = 'n'
                                break
                            elif text == "yes":
                                command_query = 'y'
                                break

                            if self.confirmation:
                                speech_txt = "Did you say " + command_query + " ? yes or no"
                                print("[System Voice] " + speech_txt)
                                self._speech(speech_txt)
                                state = 3
                                if is_test:
                                    return speech_txt
                                continue
                            else:
                                break

                        # state 3 : wait for confirmation
                        if self.confirmation and state == 3 and not text == "":
                            if "no" in text:
                                state = 2
                                command_query = ''
                                speech_txt = "Please repeat again"
                                print("[System Voice] " + speech_txt)
                                self._speech(speech_txt)
                                if is_test:
                                    return speech_txt
                                continue
                            elif "yes" in text:
                                if is_test:
                                    command_query = "testing"
                                break

                return command_query

        except KeyboardInterrupt:
            print("==> Finished Recording")
        except Exception as e:
            print(str(e))

        return "Error"

    def _record_cb(self, indata, frames, time, status):

        # if status:
        #     print(status, file=sys.stderr)

        self.q.put(bytes(indata))

    def _get_result(self):
        recognizer_result_agent = self.recognizer.Result()
        result_dict = json.loads(recognizer_result_agent)
        print("[Human Voice] " + result_dict.get('text'))
        return result_dict

    def _speech(self, text: str, _: int = 0) -> bool:

        tts_url = (
            f"https://api.streamelements.com/kappa/v2/speech?voice=Brian&text={text}"
        )
        response = requests.get(tts_url)

        if response.status_code == 200:
            if response.content is not None:
                try:
                    with open("speech_vc.mp3", "wb") as f:
                        f.write(response.content)
                    playsound("speech_vc.mp3")
                    os.remove("speech_vc.mp3")
                except:
                    print("Unable to play")
            return True
        else:
            print(
                "Request failed with status code: %s, response content: %s",
                response.status_code,
                response.content,
            )
            return False
