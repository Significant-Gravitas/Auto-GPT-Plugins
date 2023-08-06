import asyncio
import json
import os
import random
import time
import traceback
from glob import glob
import openai

from telegram import Bot, Update
from telegram.error import TimedOut
from telegram.ext import CallbackContext


if os.name == "nt":
    import soundfile as sf
else:
    import sox

from pathlib import Path

import torch
import torchaudio

from autogpt.logs import logger
from autogpt.llm.utils import count_string_tokens

response_queue = ""


def run_async(coro):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:  # 'RuntimeError: There is no current event loop...'
        loop = None
    if loop and loop.is_running():
        return loop.create_task(coro)
    else:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        return asyncio.run(coro)


def log(message):
    # print with purple color
    print("\033[95m" + str(message) + "\033[0m")


def summarize_text(text):
    """
    Summarize the given text using the GPT-3 model.
    """
    # Define the prompt for the GPT-3 model.
    prompt = (
        {
            "role": "system",
            "content": """You are a helpful assistant that summarizes text. Your task is to create a concise running summary of actions and information results in the provided text, focusing on key and potentially important information to remember.
You will receive the messages of a conversation. Combine them, adding relevant key information from the latest development in 1st person past tense and keeping the summary concise.""",
        },
        {"role": "user", "content": f"Please summarize the following text: {text}"},
    )

    # Use the OpenAI API to generate a summary.
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k", messages=prompt, max_tokens=10000
    )

    # Extract the summary from the response.
    summary = response["choices"][0]["message"]["content"]

    return summary


def chunk_text(text, max_tokens=3000):
    """Split a piece of text into chunks of a certain size."""
    chunks = []
    chunk = ""
    for message in text.split(" "):
        if (
            count_string_tokens(str(chunk) + str(message), model_name="gpt-4")
            <= max_tokens
        ):
            chunk += " " + message
        else:
            chunks.append(chunk)
            chunk = message
    chunks.append(chunk)  # Don't forget the last chunk!
    return chunks


def summarize_chunks(chunks):
    """Generate a summary for each chunk of text."""
    summaries = []
    for chunk in chunks:
        try:
            summaries.append(summarize_text(chunk))
        except Exception as e:
            log(f"Error while summarizing text: {e}")
            summaries.append(chunk)  # If summarization fails, use the original text.
    return summaries


class TelegramUtils:
    def __init__(self, api_key: str = None, chat_id: str = None):
        if not api_key:
            log(
                "No api key provided. Please set the TELEGRAM_API_KEY environment variable."
            )
            log("You can get your api key by talking to @BotFather on Telegram.")
            log(
                "For more information, please visit: https://core.telegram.org/bots/tutorial#6-botfather"
            )
            exit(1)

        self.api_key = api_key

        if not chat_id:
            log(
                "Sophie plugin: No chat id provided. Please set the TELEGRAM_CHAT_ID environment variable."
            )
            user_input = input(
                "Would you like to send a test message to your bot to get the id? (y/n): "
            )
            if user_input == "y":
                try:
                    log("Please send a message to your telegram bot now.")
                    update = self.poll_anyMessage()
                    log("Message received! Getting chat id...")
                    chat_id = update.message.chat.id
                    log("Your chat id is: " + str(chat_id))
                    log("And the message is: " + update.message.text)
                    confirmation = random.randint(1000, 9999)
                    log("Sending confirmation message: " + str(confirmation))
                    text = f"Hello! Your chat id is: {chat_id} and the confirmation code is: {confirmation}"
                    self.chat_id = chat_id
                    self._send_message(text)  # Send confirmation message
                    log(
                        "Please set the TELEGRAM_CHAT_ID environment variable to this value."
                    )
                except TimedOut:
                    log(
                        "Error while sending test message. Please check your Telegram bot."
                    )
        self.chat_id = chat_id
        self._setup_speech()
        self.load_conversation_history()
        self.add_to_conversation_history("Sophie has been restarted.")
        self.send_message("Waking up...")

    def get_previous_message_history(self):
        """Get the previous message history."""
        try:
            if len(self.conversation_history) == 0:
                return "There is no previous message history."

            tokens = count_string_tokens(
                str(self.conversation_history), model_name="gpt-4"
            )
            if tokens > 3000:
                log("Message history is over 3000 tokens. Summarizing...")
                chunks = chunk_text(str(self.conversation_history))
                summaries = summarize_chunks(chunks)
                summarized_history = " ".join(summaries)
                summarized_history += " " + " ".join(self.conversation_history[-6:])
                return summarized_history

            return self.conversation_history
        except Exception as e:
            log(f"Error while getting previous message history: {e}")
            log(traceback.format_exc())
            exit(1)

    def load_conversation_history(self):
        """Load the conversation history from a file."""
        try:
            with open("conversation_history.json", "r") as f:
                self.conversation_history = json.load(f)
        except FileNotFoundError:
            # If the file doesn't exist, create it.
            self.conversation_history = []
        log("Loaded conversation history:")
        log(self.conversation_history)

    def save_conversation_history(self):
        """Save the conversation history to a file."""
        with open("conversation_history.json", "w") as f:
            json.dump(self.conversation_history, f)

    def add_to_conversation_history(self, message):
        """Add a message to the conversation history and save it."""
        self.conversation_history.append(message)
        self.save_conversation_history()

    def _decode_voice(self, voice_file):
        """Set up the STT model."""
        try:
            log("Setting up...")
            device = torch.device("cpu")
            torch.set_num_threads(4)
            # Load the model.
            log("Loading model...")
            model, decoder, utils = torch.hub.load(
                repo_or_dir="snakers4/silero-models",
                model="silero_stt",
                language="en",  # also available 'de', 'es'
                device=device,
            )

            (read_batch, split_into_batches, read_audio, prepare_model_input) = utils
            test_files = glob(voice_file)
            batches = split_into_batches(test_files, batch_size=10)
            input = prepare_model_input(read_batch(batches[0]), device=device)
            output = model(input)

            text_result = ""
            for sample in output:
                text_result += decoder(sample.cpu())
            log("voice recognition complete: " + text_result)
            return text_result
        except Exception as e:
            log(e)
            log(traceback.format_exc())
            log(f"if it's no audio backend: {str(torchaudio.get_audio_backend())}")
            exit(1)

    def _setup_speech(self):
        """Set up the TTS model."""

        log("Setting up...")
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        torch.set_num_threads(4)
        local_file = "model.pt"

        # Download the model if it doesn't exist locally.
        if not os.path.isfile(local_file):
            log("Downloading model...")
            torch.hub.download_url_to_file(
                "https://models.silero.ai/models/tts/en/v3_en.pt", local_file
            )

        # Load the model.
        log("Loading model...")
        self.model = torch.package.PackageImporter(local_file).load_pickle(
            "tts_models", "model"
        )
        self.model.to(device)
        self.voice = "en_10"
        log("Setup speech complete.")

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
            log(f"Generating speech for chunk {i + 1} of {len(chunks)}...")
            output_file = output_dir / f"book_{int(time.time())}_{i}.wav"

            self.model.save_wav(
                text=chunk,
                speaker=speaker,
                sample_rate=sample_rate,
                audio_path=str(output_file),
            )
            log("Speech generated, converting to ogg...")

            local_string = str("./")
            # if Windows, change to .\\
            if os.name == "nt":
                local_string = str(".\\")

            self.send_voice(local_string + str(output_file))

    def poll_anyMessage(self):
        logger.info("Waiting for first message...")
        return run_async(self.poll_anyMessage_async())

    async def poll_anyMessage_async(self):
        bot = Bot(token=self.api_key)
        last_update = await bot.get_updates(timeout=30)
        if len(last_update) > 0:
            last_update_id = last_update[-1].update_id
        else:
            last_update_id = -1

        while True:
            try:
                log("Waiting for first message...")
                updates = await bot.get_updates(offset=last_update_id + 1, timeout=30)
                for update in updates:
                    if update.message:
                        return update
            except Exception as e:
                log(f"Error while polling updates: {e}")

            await asyncio.sleep(1)

    def is_authorized_user(self, update: Update):
        return update.effective_user.id == int(self.chat_id)

    def handle_response(self, update: Update, context: CallbackContext):
        try:
            log("Received response: " + update.message.text)

            if self.is_authorized_user(update):
                response_queue.put(update.message.text)
        except Exception as e:
            log(e)

    async def delete_old_messages(self):
        bot = await self.get_bot()
        updates = await bot.get_updates(offset=0)
        count = 0
        for update in updates:
            try:
                log(
                    "Deleting message: "
                    + update.message.text
                    + " "
                    + str(update.message.message_id)
                )
                await bot.delete_message(
                    chat_id=update.message.chat.id, message_id=update.message.message_id
                )
            except Exception as e:
                log(
                    f"Error while deleting message: {e} \n"
                    + f" update: {update} \n {traceback.format_exc()}"
                )
            count += 1
        if count > 0:
            log("Cleaned up old messages.")

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

    def _send_message(self, message, speak=False):
        try:
            run_async(self._send_message_async(message=message))
            if speak:
                self._speech(message)
        except Exception as e:
            log(f"Error while sending message: {e}")
            return "Error while sending message."

    async def _send_voice_async(self, voice_file):
        try:
            bot = await self.get_bot()
            await bot.send_voice(chat_id=self.chat_id, voice=open(voice_file, "rb"))
        except RuntimeError:
            log("Error while sending voice message")

    def send_voice(self, voice_file):
        try:
            run_async(self._send_voice_async(voice_file))
        except RuntimeError as e:
            log(e)
            log(traceback.format_exc())
            log("Error while sending voice message")
            return "Error while sending voice message."

    async def _send_message_async(self, message, speak=False):
        log("Sending message to Telegram.. ")
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

        log("Asking user: " + prompt)
        await self._send_message_async(message=prompt, speak=speak)

        log("Waiting for response on Telegram chat...")
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

        log("Response received from Telegram: " + response_text)
        return response_text

    async def check_voice(self, update: Update):
        if update.message.voice:
            file_id = update.message.voice.file_id
            bot = Bot(token=self.api_key)
            newFile = await bot.get_file(file_id)
            await newFile.download_to_drive("./speech.ogg")
            await self._send_message_async(
                "I am listening to your voice message, one second! :)"
            )
            return True
        else:
            return False

    async def _poll_updates(self):
        global response_queue
        bot = await self.get_bot()
        log("getting updates...")

        last_update = await bot.get_updates(timeout=10)
        if len(last_update) > 0:
            last_messages = [u.message.text for u in last_update]
            # last_messages failes when text or message is not given, rewrite with a checker and also log the object
            last_messages = []
            for u in last_update:
                if u.message:
                    if u.message.text:
                        last_messages.append(u.message.text)
                    else:
                        log("no text in message in update: " + str(u))
            # itarate and check if last messages are already known, if not add to history
            for message in last_messages:
                if message not in self.conversation_history:
                    self.conversation_history.append("Message by User: " + message)

            log("last messages: " + str(last_messages))
            last_update_id = last_update[-1].update_id

        else:
            last_update_id = -1

        log("last update id: " + str(last_update_id))
        while True:
            try:
                log("Polling updates...")
                updates = await bot.get_updates(offset=last_update_id + 1, timeout=30)
                for update in updates:
                    if self.is_authorized_user(update):
                        if update.message and update.message.text:
                            response_queue = update.message.text
                            self.add_to_conversation_history("User: " + response_queue)
                            return response_queue
                        elif update.message and await self.check_voice(update):
                            log(
                                "Voice message received, it should be saved as speech.ogg"
                            )
                            response_queue = "Received voice message: "
                            response_queue += self._decode_voice("./speech.ogg")
                            self.add_to_conversation_history(
                                "User voice message: " + response_queue
                            )
                            return response_queue

                    last_update_id = max(last_update_id, update.update_id)
            except Exception as e:
                log(f"Error while polling updates: {e}")

            await asyncio.sleep(1)

    def idle_until_interaction(self):
        """Interface method for Auto-GPT.
        Wait for user interaction and return the answer."""
        self.send_message("* Sleeping... *")
        answer = "User did not respond."
        try:
            answer = run_async(self._poll_updates())
        except Exception as e:
            log(traceback.format_exc())
            log(f"Error while polling updates: {e}")
            return answer + "Error while waiting for interaction. Use ask_user instead."
        self.add_to_conversation_history("Received while sleeping: " + answer)
        return answer

    def send_message(self, message):
        """Interface method for sending a message."""
        self.add_to_conversation_history("Sent: " + message)
        self._send_message(message + "...")
        return "Sent message successfully."

    def send_message_and_speak(self, message):
        """Interface method for sending a message and send a voice message."""
        self.add_to_conversation_history("Sent via voicemessage: " + message)
        self._send_message(message + "...", speak=True)
        return "Sent message successfully."

    def ask_user(self, prompt):
        """Interface Method for Auto-GPT.
        Ask the user a question, return the answer"""
        self.add_to_conversation_history("Asked: " + prompt)
        answer = "User has not answered."
        try:
            answer = run_async(self.ask_user_async(prompt=prompt))
        except TimedOut:
            log("Telegram timeout error, trying again...")
            answer = self.ask_user(prompt=prompt)
        return answer

    def ask_user_voice(self, prompt):
        """Interface Method for Auto-GPT.
        Ask the user a question and send a voice message, return the answer"""
        log("Asking user: " + prompt)
        self.add_to_conversation_history("Asked via voicemessage: " + prompt)
        answer = "User has not answered."
        try:
            answer = run_async(self.ask_user_async(prompt=prompt, speak=True))
        except TimedOut:
            log("Telegram timeout error, trying again...")
            answer = self.ask_user(prompt=prompt, speak=True)
        except RuntimeError:
            answer = "Runtime Error while asking user"
        return answer


if __name__ == "__main__":
    telegram_api_key = os.getenv("TELEGRAM_SOPHIE_API_KEY")
    telegram_chat_id = os.getenv("TELEGRAM_SOPHIE_CHAT_ID")
    telegram_utils = TelegramUtils(chat_id=telegram_chat_id, api_key=telegram_api_key)
    telegram_utils._send_message("Hello World!")
