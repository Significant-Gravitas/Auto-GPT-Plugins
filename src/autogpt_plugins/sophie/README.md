# AutoGPT Sophie Plugin
Simple planning commands for planning leveraged with chatgpt3.5 and json objects to keep track of its progress on a list of tasks.
![image](https://github.com/Wladastic/Auto-GPT-Plugins/assets/11997278/16c7cb86-0a1f-4aae-a485-f40a1aa6506c)
![image](https://github.com/Wladastic/Auto-GPT-Plugins/assets/11997278/249ae4de-e3c6-4c8a-95b3-93348472978d)


### Getting started
1. Install the plugin
```

Remember to also update your .env to include 

```
ALLOWLISTED_PLUGINS=SophieTelegram
TELEGRAM_SOPHIE_API_KEY=<your telegram bot api key>
TELEGRAM_SOPHIE_CHAT_ID=<your telegram chat id>
```

2. Modify your yaml file to include the following
```
  - Prefer ask_user and send_message to remain in the conversation unless the User gave you a task, then you have to update him on what you are doing.
  - As User might be multilangual, If you use ask_user_voice or send_message_voice, then speak English, but if you use ask_user or send_message, then respond in the language the User used.


