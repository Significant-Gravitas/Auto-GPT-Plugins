import asyncio
import os
import random
import time
import traceback
from glob import glob

from telegram import Bot, Update
from telegram.error import TimedOut
from telegram.ext import CallbackContext

# if os is windows, install soundfile, if not, install sox
if os.name == "nt":
    import soundfile as sf
else:
    import sox

from pathlib import Path

import torch
import torchaudio

from autogpt.logs import logger

response_queue = ""


class TelegramUtils:
    def __init__(self, api_key: str = None, chat_id: str = None):
        if not api_key:
            print(
                "No api key provided. Please set the TELEGRAM_API_KEY environment variable."
            )
            print("You can get your api key by talking to @BotFather on Telegram.")
            print(
                "For more information, please visit: https://core.telegram.org/bots/tutorial#6-botfather"
            )
            exit(1)

        self.api_key = api_key

        if not chat_id:
            print(
                "TELEGRAM PLUGIN: No chat id provided. Please set the TELEGRAM_CHAT_ID environment variable."
            )
            user_input = input(
                "Would you like to send a test message to your bot to get the id? (y/n): "
            )
            if user_input == "y":
                try:
                    print("Please send a message to your telegram bot now.")
                    update = self.poll_anyMessage()
                    print("Message received! Getting chat id...")
                    chat_id = update.message.chat.id
                    print("Your chat id is: " + str(chat_id))
                    print("And the message is: " + update.message.text)
                    confirmation = random.randint(1000, 9999)
                    print("Sending confirmation message: " + str(confirmation))
                    text = f"Hello! Your chat id is: {chat_id} and the confirmation code is: {confirmation}"
                    self.chat_id = chat_id
                    self._send_message(text)  # Send confirmation message
                    print(
                        "Please set the TELEGRAM_CHAT_ID environment variable to this value."
                    )
                except TimedOut:
                    print(
                        "Error while sending test message. Please check your Telegram bot."
                    )
            exit(1)
        self.chat_id = chat_id
        self._setup_speech()
        # self.send_message( "Hey, sorry! \n I think I fell asleep, but I'm awake now! \n I'll be ready in a few seconds.")

    def _decode_voice(self, voice_file):
        """Set up the STT model."""
        try:
            print("Setting up...")
            device = torch.device("cpu")
            torch.set_num_threads(4)
            # Load the model.
            print("Loading model...")
            model, decoder, utils = torch.hub.load(
                repo_or_dir="snakers4/silero-models",
                model="silero_stt",
                language="en",  # also available 'de', 'es'
                device=device,
            )

            (read_batch, split_into_batches,
            read_audio, prepare_model_input) = utils
            test_files = glob(voice_file)
            batches = split_into_batches(test_files, batch_size=10)
            input = prepare_model_input(read_batch(batches[0]),
                            device=device)
            output = model(input)

            text_result = ""
            for sample in output:
                text_result += decoder(sample.cpu())
            print("voice recognition complete: " + text_result)
            return text_result
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            print(f"if it's no audio backend: {str(torchaudio.get_audio_backend())}")
            exit(1)

    def _setup_speech(self):
        """Set up the TTS model."""

        print("Setting up...")
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        torch.set_num_threads(4)
        local_file = "model.pt"

        # Download the model if it doesn't exist locally.
        if not os.path.isfile(local_file):
            print("Downloading model...")
            torch.hub.download_url_to_file(
                "https://models.silero.ai/models/tts/en/v3_en.pt", local_file
            )

        # Load the model.
        print("Loading model...")
        self.model = torch.package.PackageImporter(local_file).load_pickle(
            "tts_models", "model"
        )
        self.model.to(device)
        self.voice = "en_10"
        print("Setup speech complete.")

    def _speech(self, text: str):
        """Generate speech from text using the TTS model."""

        # Replace common emoticons with words.
        text = text.replace(":)", "smiley face")

        sample_rate = 48000
        speaker = self.voice

        # Create output directory if it doesn't exist.
        output_dir = Path("./speech")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Split the text into chunks of 1000 symbols or less.
        chunks = [text[i : i + 1000] for i in range(0, len(text), 1000)]

        # Generate speech for each chunk.
        for i, chunk in enumerate(chunks):
            # Save generated speech to a .wav file.
            print(f"Generating speech for chunk {i + 1} of {len(chunks)}...")
            output_file = output_dir / f"book_{int(time.time())}_{i}.wav"

            self.model.save_wav(
                text=chunk,
                speaker=speaker,
                sample_rate=sample_rate,
                audio_path=str(output_file),
            )

            # Play the generated speech.
            # playsound(audio, True)
            print("Speech generated, converting to ogg...")

            local_string = str("./")
            # if Windows, change to .\\
            if os.name == "nt":
                local_string = str(".\\")

            self.send_voice(local_string + str(output_file))

            # ogg_file = convert_wav_to_ogg(local_string + str(output_file))
            # if ogg_file:
            #    print("Converted to ogg, sending to telegram...")
            #    self.send_voice(ogg_file)
            # else:

    def poll_anyMessage(self):
        logger.info("Waiting for first message...")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(self.poll_anyMessage_async())

    async def poll_anyMessage_async(self):
        bot = Bot(token=self.api_key)
        last_update = await bot.get_updates(timeout=30)
        if len(last_update) > 0:
            last_update_id = last_update[-1].update_id
        else:
            last_update_id = -1

        while True:
            try:
                print("Waiting for first message...")
                updates = await bot.get_updates(offset=last_update_id + 1, timeout=30)
                for update in updates:
                    if update.message:
                        return update
            except Exception as e:
                print(f"Error while polling updates: {e}")

            await asyncio.sleep(1)

    def is_authorized_user(self, update: Update):
        return update.effective_user.id == int(self.chat_id)

    def handle_response(self, update: Update, context: CallbackContext):
        try:
            print("Received response: " + update.message.text)

            if self.is_authorized_user(update):
                response_queue.put(update.message.text)
        except Exception as e:
            print(e)

    async def delete_old_messages(self):
        bot = await self.get_bot()
        updates = await bot.get_updates(offset=0)
        count = 0
        for update in updates:
            try:
                print(
                    "Deleting message: "
                    + update.message.text
                    + " "
                    + str(update.message.message_id)
                )
                await bot.delete_message(
                    chat_id=update.message.chat.id, message_id=update.message.message_id
                )
            except Exception as e:
                print(
                    f"Error while deleting message: {e} \n"
                    + f" update: {update} \n {traceback.format_exc()}"
                )
            count += 1
        if count > 0:
            print("Cleaned up old messages.")

    async def get_bot(self):
        bot_token = self.api_key
        bot = Bot(token=bot_token)
        commands = await bot.get_my_commands()
        if len(commands) == 0:
            await self.set_commands(bot)
        return bot

    async def set_commands(self, bot):
        await bot.set_my_commands(
            [
                ("start", "Start Auto-GPT"),
                ("stop", "Stop Auto-GPT"),
                ("help", "Show help"),
            ]
        )

    def idle_until_interaction(self):
        self.send_message("* Sleeping... *")
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError as e:
            loop = None
        if loop and loop.is_running():
            print("Running idle_until_interaction async")
            return loop.create_task(self._poll_updates())
        else:
            print("Running idle_until_interaction sync")
            try:
                eventloop = asyncio.get_event_loop()
            except RuntimeError:
                eventloop = None
            try:
                if eventloop and hasattr(eventloop, "is_running"):
                    if eventloop.is_running():
                        return eventloop.create_task(self._poll_updates())
                    else:
                        return eventloop.run_until_complete(self._poll_updates())
                else:
                    return asyncio.run(self._poll_updates())
            except Exception as e:
                print(f"Error while polling updates: {e}")

    def send_message(self, message):
        self._send_message(message + "...")
        return "Sent message successfully."

    def send_message_and_speak(self, message):
        self._send_message(message + "...", speak=True)
        return "Sent message successfully."

    def _send_message(self, message, speak=False):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError as e:  # 'RuntimeError: There is no current event loop...'
            loop = None

        if loop and loop.is_running():
            print(
                "Sending message async, if this fials its due to rununtil complete task"
            )
            loop.create_task(self._send_message_async(message=message))
        else:
            print("Sending message sync, if this fials its due to asyncio run")
            try:
                eventloop = asyncio.get_event_loop()
            except RuntimeError:  # 'RuntimeError: There is no current event loop...'
                eventloop = None
            try:
                if (
                    eventloop
                    and hasattr(eventloop, "run_until_complete")
                    and eventloop.is_running()
                ):
                    print("Event loop is running")
                    eventloop.run_until_complete(
                        self._send_message_async(message=message)
                    )
                else:
                    asyncio.run(self._send_message_async(message=message))
            except Exception as e:
                print(f"Error while sending message: {e}")
        if speak:
            self._speech(message)

    async def _send_voice_async(self, voice_file):
        try:
            bot = await self.get_bot()
            await bot.send_voice(chat_id=self.chat_id, voice=open(voice_file, "rb"))
        except RuntimeError:
            print("Error while sending voice message")

    def send_voice(self, voice_file):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:  # 'RuntimeError: There is no current event loop...'
            loop = None
        try:
            if loop and loop.is_running():
                print(
                    "Sending voice message async, if this fials its due to rununtil complete task"
                )
                loop.create_task(self._send_voice_async(voice_file))
            else:
                print(
                    "Sending voice message sync, if this fials its due to asyncio run"
                )
                eventloop = asyncio.get_event_loop
                if hasattr(eventloop, "run_until_complete") and eventloop.is_running():
                    print("Event loop is running")
                    eventloop.run_until_complete(self._send_voice_async(voice_file))
                else:
                    asyncio.run(self._send_voice_async(voice_file))

        except RuntimeError as e:
            print(e)
            print(traceback.format_exc())
            print("Error while sending voice message")
            pass

    async def _send_message_async(self, message, speak=False):
        print("Sending message to Telegram.. ")
        recipient_chat_id = self.chat_id
        bot = await self.get_bot()

        # properly handle messages with more than 2000 characters by chunking them
        if len(message) > 2000:
            message_chunks = [
                message[i : i + 2000] for i in range(0, len(message), 2000)
            ]
            for message_chunk in message_chunks:
                await bot.send_message(chat_id=recipient_chat_id, text=message_chunk)
        else:
            await bot.send_message(chat_id=recipient_chat_id, text=message)
        if speak:
            self._speech(message)

    async def ask_user_async(self, prompt, speak=False):
        global response_queue

        response_queue = ""
        # await delete_old_messages()

        print("Asking user: " + prompt)
        await self._send_message_async(message=prompt, speak=speak)

        print("Waiting for response on Telegram chat...")
        await self._poll_updates()

        if response_queue == "/start":
            response_queue = await self.ask_user(
                self,
                prompt="I am already here... \n Please use /stop to stop me first.",
            )
        if response_queue == "/help":
            response_queue = await self.ask_user(
                self,
                prompt="You can use /stop to stop me \n and /start to start me again.",
            )
        if response_queue == "/auto":
            return "s"
        if response_queue == "/stop":
            await self._send_message_async("Okay, I will go to sleep now.")
            exit(0)
        elif response_queue == "/yes":
            response_text = "yes"
            response_queue = "yes"
        elif response_queue == "/no":
            response_text = "no"
            response_queue = "no"
        response_text = response_queue

        print("Response received from Telegram: " + response_text)
        return response_text

    async def check_voice(self, update: Update):
        if update.message.voice:
            file_id = update.message.voice.file_id
            bot = Bot(token=self.api_key)
            newFile = await bot.get_file(file_id)
            await newFile.download_to_drive("./speech.ogg")
            await self._send_message_async("I am listening to your voice message, one second! :)")
            return True
        else:
            return False

    async def _poll_updates(self):
        global response_queue
        bot = await self.get_bot()
        print("getting updates...")

        last_update = await bot.get_updates(timeout=10)
        if len(last_update) > 0:
            print("last updates: " + str(last_update))
            last_update_id = last_update[-1].update_id
            # print all messages in last updates
            for update in last_update:
                print(update.message.text)    
        else:
            last_update_id = -1

        print("last update id: " + str(last_update_id))
        while True:
            try:
                print("Polling updates...")
                updates = await bot.get_updates(offset=last_update_id + 1, timeout=30)
                for update in updates:
                    if self.is_authorized_user(update):
                        if update.message and update.message.text:
                            response_queue = update.message.text
                            return response_queue
                        elif update.message and await self.check_voice(update):
                            print(
                                "Voice message received, it should be saved as speech.ogg"
                            )
                            response_queue = "Received voice message: " 
                            response_queue += self._decode_voice("./speech.ogg")
                            return response_queue

                    last_update_id = max(last_update_id, update.update_id)
            except Exception as e:
                print(f"Error while polling updates: {e}")

            await asyncio.sleep(1)

    def ask_user(self, prompt):
        print("Asking user: " + prompt)
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:  # 'RuntimeError: There is no current event loop...'
            loop = None
        try:
            if loop and loop.is_running():
                return loop.create_task(self.ask_user_async(prompt=prompt))
            else:
                return asyncio.run(self.ask_user_async(prompt=prompt))
        except TimedOut:
            print("Telegram timeout error, trying again...")
            return self.ask_user(prompt=prompt)

    def ask_user_voice(self, prompt):
        print("Asking user: " + prompt)
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:  # 'RuntimeError: There is no current event loop...'
            loop = None
        try:
            if loop and loop.is_running():
                return loop.create_task(self.ask_user_async(prompt=prompt, speak=True))
            else:
                return asyncio.run(self.ask_user_async(prompt=prompt, speak=True))
        except TimedOut:
            print("Telegram timeout error, trying again...")
            return self.ask_user(prompt=prompt, speak=True)
        except RuntimeError:
            print("Error while asking user")


if __name__ == "__main__":
    telegram_api_key = os.getenv("TELEGRAM_SOPHIE_API_KEY")
    telegram_chat_id = os.getenv("TELEGRAM_SOPHIE_CHAT_ID")
    telegram_utils = TelegramUtils(chat_id=telegram_chat_id, api_key=telegram_api_key)
    telegram_utils._send_message("Hello World!")
