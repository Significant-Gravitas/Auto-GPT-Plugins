# speech_to_text_plugin.py

import os
import pyaudio
import io
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums
from google.cloud.speech_v1p1beta1 import types

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'

def transcribe_streaming(stream):
    client = speech.SpeechClient()
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US')
    streaming_config = types.StreamingRecognitionConfig(config=config)

    requests = (types.StreamingRecognizeRequest(audio_content=chunk) for chunk in stream)
    responses = client.streaming_recognize(streaming_config, requests)

    for response in responses:
        if response.results:
            return response.results[0].alternatives[0].transcript
    return None

def record_audio():
    RATE = 16000
    CHUNK = int(RATE / 10)
    FORMAT = pyaudio.paInt16
    CHANNELS = 1

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    while True:
        data = stream.read(CHUNK)
        yield data

if __name__ == '__main__':
    print("Recording... Press Ctrl+C to stop.")
    try:
        for data in record_audio():
            transcript = transcribe_streaming(io.BytesIO(data))
            if transcript:
                print("Transcript:", transcript)
    except KeyboardInterrupt:
        pass
