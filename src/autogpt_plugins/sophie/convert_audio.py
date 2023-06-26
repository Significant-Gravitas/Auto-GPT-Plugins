"""
Author        :Julio Sanz
Website       :www.elarraydejota.com
Email         :juliojosesb@gmail.com
Description   :Convert wav audio file to ogg
Dependencies  :This script has been written using Python 2.7.9
Usage         :python wav_to_ogg.py /path/to/file.wav
Example       :python wav_to_ogg.py /home/bob/Music/mysong.wav
License       :GPLv3
"""

import os
import sys
import traceback

from pydub import AudioSegment


def convert_wav_to_ogg(file_path):
    AudioSegment.converter = "C:\\ffmpeg\\bin\\ffmpeg.exe"
    # convert file_path to absolute path
    file_path = os.path.abspath(file_path)
    print(f"Converting wav to ogg: {file_path}")
    orig_file = file_path
    dest_song = os.path.splitext(file_path)[0] + ".ogg"
    print(f"dest_song: {dest_song}")
    song = AudioSegment.from_wav(orig_file)
    try:
        song.export(dest_song, format="ogg")
    except Exception as e:
        print(f"Error converting wav to ogg: {e}")
        print(traceback.format_exc())
        exit(1)
    print(f"Converted wav to ogg: {dest_song}")
    return dest_song


if __name__ == "__main__":
    convert_wav_to_ogg()
