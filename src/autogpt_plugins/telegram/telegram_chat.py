import asyncio
import traceback

from telegram import Bot, Update
from telegram.error import TimedOut
from telegram.ext import CallbackContext

response_queue = ""


class TelegramUtils:
    def __init__(self, api_key: str = None, chat_id: str = None):
        self.api_key = api_key
        self.chat_id = chat_id

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
        commands = await bot.get_my_commands()
        return bot

    async def set_commands(self, bot):
        await bot.set_my_commands(
            [
                ("start", "Start Auto-GPT"),
                ("stop", "Stop Auto-GPT"),
                ("help", "Show help"),
                ("yes", "Confirm"),
                ("no", "Deny"),
            ]
        )

    def send_message(self, message):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:  # 'RuntimeError: There is no current event loop...'
            loop = None
        if loop and loop.is_running():
            loop.create_task(self._send_message(message=message))
        else:
            asyncio.run(self._send_message(message=message))

    def send_voice(self, voice_file):
        try:
            self.get_bot().send_voice(
                chat_id=self.chat_id, voice=open(voice_file, "rb")
            )
        except RuntimeError:
            print("Error while sending voice message")

    async def _send_message(self, message):
        print("Sending message to Telegram.. ")
        recipient_chat_id = self.chat_id
        bot = await self.get_bot()
        await bot.send_message(chat_id=recipient_chat_id, text=message)

    async def ask_user_async(self, prompt):
        global response_queue
        question = prompt + " \n Confirm: /yes     Decline: /no \n Or type your answer."

        response_queue = ""
        # await delete_old_messages()

        print("Asking user: " + question)
        self.send_message(message=question)

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

        if response_queue == "/stop":
            self.send_message("Stopping Auto-GPT now!")
            exit(0)
        elif response_queue == "/yes":
            response_text = "yes"
            response_queue = "yes"
        elif response_queue == "/no":
            response_text = "no"
            response_queue = "no"
        if response_queue.capitalize() in [
            "Yes",
            "Okay",
            "Ok",
            "Sure",
            "Yeah",
            "Yup",
            "Yep",
        ]:
            response_text = "y"
        elif response_queue.capitalize() in ["No", "Nope", "Nah", "N"]:
            response_text = "n"
        else:
            response_text = response_queue

        print("Response received from Telegram: " + response_text)
        return response_text

    async def _poll_updates(self):
        global response_queue
        bot = await self.get_bot()

        last_update = await bot.get_updates(timeout=30)
        if len(last_update) > 0:
            last_update_id = last_update[-1].update_id
        else:
            last_update_id = 0

        while True:
            try:
                print("Polling updates...")
                updates = await bot.get_updates(offset=last_update_id + 1, timeout=30)
                for update in updates:
                    if update.message and update.message.text:
                        if self.is_authorized_user(update):
                            response_queue = update.message.text
                            return
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
