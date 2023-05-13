# Changes: 
This repository contains various plugins developed for use with the AutoGPT model. These plugins extend the functionality of AutoGPT by providing additional features, such as speech-to-text transcription, integration with external APIs, and more.

## Table of Contents

1. [Speech-to-Text Plugin](#speech-to-text-plugin)
2. [Installation](#installation)
3. [Contributing](#contributing)
4. [License](#license)

## Speech-to-Text Plugin

The speech-to-text plugin allows users to transcribe spoken input in real-time and feed the transcribed text into the AutoGPT model for processing. This plugin uses the Google Cloud Speech-to-Text API for transcription and PyAudio for real-time audio recording from the user's microphone.

### Features

- Real-time audio recording from the user's microphone
- Transcription of spoken input using Google Cloud Speech-to-Text API
- Integration with the AutoGPT model for processing transcribed text

### Usage

1. Set up the Google Cloud Speech-to-Text API and obtain your API credentials as a JSON file.
2. Update the `speech_to_text_plugin.py` file to use the correct path to your API credentials.
3. Install the required dependencies: `pip install google-cloud-speech pyaudio`
4. Run the `speech_to_text_plugin.py` file to start recording and transcribing audio input.

## Installation

To install the plugins, follow these steps:

1. Clone this repository: `git clone https://github.com/Significant-Gravitas/Auto-GPT`
2. Navigate to the `src/autogpt_plugins` directory.
3. Install the required dependencies for each plugin as specified in their respective README files or source code comments.

## Contributing

Nigel Phillips a.k.a. Swooshcode
Software Developer
Founder of Frame Tech Solutions Ltd., Co. 框架技術解決方案
For inquiries: https://tinyurl.com/nigelphillips

## License

MIT License

Copyright (c) 2023 Toran Bruce Richards

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
