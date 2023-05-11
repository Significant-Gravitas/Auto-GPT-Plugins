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
        self.confirmation = True

        print("Display input/output devices")
        print(sd.query_devices())
        print(sd.default.device[0])
        device_info = sd.query_devices(sd.default.device[0], 'input')
        self.samplerate = int(device_info['default_samplerate'])

        if os.getenv("VOICE_COMMAND_INITCALL"):
            self.initiator = os.getenv("VOICE_COMMAND_INITCALL")

        if os.getenv("VOICE_COMMAND_CONFIRM") and os.getenv("VOICE_COMMAND_CONFIRM") == "True":
            self.confirmation = True

        print("==> Initial Default Device Number:{} Desc:{}".format(sd.default.device[0], device_info))

        self.q = queue.Queue()

        self.init_model()

    def init_model(self):

        try:
            self.model = Model(r"./model")
            self.recognizer = KaldiRecognizer(self.model, self.samplerate)
            self.recognizer.SetWords(False)
        except Exception as e:
            print('MODEL_INIT_ERROR')

    def run(self) -> str:

        print("==> Begin recording. Press Ctrl+C to stop the recording ")
        try:
            with sd.RawInputStream(dtype='int16', channels=1, callback=self._record_cb):

                command_query = 'None'

                # state 1 : wait for init call
                # state 2 : wait for question
                # state 3 : wait for confirmation

                state = 1

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
                            continue

                        # state 2 : wait for question
                        if state == 2 and not text == "" and "yes sir" not in text:
                            command_query = text
                            if self.confirmation:
                                speech_txt = "Did you say " + command_query + " ?"
                                print("[System Voice] " + speech_txt)
                                self._speech(speech_txt)
                                state = 3
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
                                continue
                            elif "yes" in text:
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
            with open("speech_vc.mp3", "wb") as f:
                f.write(response.content)
            playsound("speech_vc.mp3")
            os.remove("speech_vc.mp3")
            return True
        else:
            print(
                "Request failed with status code: %s, response content: %s",
                response.status_code,
                response.content,
            )
            return False
