# autogpt-voice-command

A plugin adding voice command integration into Auto GPT

## Features (more coming soon!)

- speak through microphone with auto-gpt
- support kaldi recognizer library

## Installation

1. Clone this repo as instructed in the main repository
2. Add this chunk of code along with your voice command API information to the `.env` file within AutoGPT:

```
CHAT_MESSAGES_ENABLED=True

... 

################################################################################
### VOICE COMMAND
################################################################################

VOICE_COMMAND_ENABLE=True
VOICE_COMMAND_SDK=kaldi
VOICE_COMMAND_INITCALL=hello
VOICE_COMMAND_CONFIRM=True
```

- VOICE_COMMAND_ENABLE is used to enable to voice command plugin
- VOICE_COMMAND_SDK is used to determine which library used for the speech recognition. Currently only kaldi is
  available and fully tested
- VOICE_COMMAND_INITCALL is used to wake the system up before providing any question
- VOICE_COMMAND_CONFIRM is used to enable confirmation on user's question before sending to autogpt. Due to the accent
  or vocabulary limitation, the library may wrongly recognize speech text from user, so user can repeat the question if
  necessary

3. Download vosk model from https://alphacephei.com/vosk/models to the autogpt root directory
4. Extract the model and rename the directory to 'model'

```
For example:

Change directory to Auto-GPT based folder
# cd Auto-GPT  

Copy the downloaded model
# cp ~/vosk-model-small-en-us-0.15.zip .

Unzip the model file
# unzip vosk-model-small-en-us-0.15.zip

Rename the model's name
# mv vosk-model-small-en-us-0.15 model
```
