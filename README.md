# Auto-GPT-Plugins


> ⚠️💀 **WARNING** 💀⚠️:
> Review the code of any plugin you use thoroughly, as plugins can execute any Python code, potentially leading to malicious activities, such as stealing your API keys.

## Installation

Download this repository as a .zip file, copy it to ./plugins/, and rename it to [Auto-GPT-Plugins.zip](https://github.com/Significant-Gravitas/Auto-GPT/archive/refs/heads/master.zip)

To download it directly from your Auto-GPT directory, you can run this command on Linux or MacOS:

```
curl -o ./plugins/Auto-GPT-Plugins.zip https://github.com/Significant-Gravitas/Auto-GPT/archive/refs/heads/master.zip
```

In PowerShell:

```
Invoke-WebRequest -Uri "https://github.com/Significant-Gravitas/Auto-GPT/archive/refs/heads/master.zip" -OutFile "./plugins/Auto-GPT-Plugins.zip"
```

Clone this repository into the plugins direcory of [Auto-GPT](https://github.dev/Significant-Gravitas/Auto-GPT).

## Plugins in the repository

For interactionless use, set `ALLOWLISTED_PLUGINS=example-plugin1,example-plugin2,example-plugin3` in your `.env`


| Plugin       | Description     | Location |
|--------------|-----------|--------|
| Twitter      | AutoGPT is capable of retrieving Twitter posts and other related content by accessing the Twitter platform via the v1.1 API using Tweepy.| [autogpt_plugins/twitter](https://github.com/Significant-Gravitas/Auto-GPT-Plugins/tree/master/src/autogpt_plugins/twitter)

## Third party plugins:
Some third-party plugins have been created by contributors that are not included in this repository. For more information about these plugins, please visit their respective GitHub pages.

| Plugin       | Description     | Repository |
|--------------|-----------------|-------------|
| System Information      | This plugin adds an extra line to the prompt, serving as a hint for the AI to use shell commands likely supported by the current system. By incorporating this plugin, you can ensure that the AI model provides more accurate and system-specific shell commands, improving its overall performance and usefulness. | [hdkiller/Auto-GPT-SystemInfo](https://github.com/hdkiller/Auto-GPT-SystemInfo) |
| Notion      | Notion plugin for Auto-GPT.  | [doutv/Auto-GPT-Notion](https://github.com/doutv/Auto-GPT-Notion) |
| Email Plugin | Revolutionize Your Email Management with Auto-GPT | [riensen/Auto-GPT-Email-Plugin](https://github.com/riensen/Auto-GPT-Email-Plugin)
| Telegram | A smoothly working Telegram bot that gives you all the messages you would normally get through the Terminal. | [Wladastic/Auto-GPT-Telegram-Plugin](https://github.com/Wladastic/Auto-GPT-Telegram-Plugin)

## Configuration

For interactionless use, set `ALLOWLISTED_PLUGINS=example-plugin1,example-plugin2,etc` in your `.env` file. 

## Making a plugin

Making a plugin is amazing! There's two routes to follow, first-party or third-party. First-party plugins are included in this repo and get included by default with all other plugins when the plugin platform is installed. Third-party plugins need to be added individually. Use first party plugins for plugins you expect others to use and want, and third party for things specifc to you. 

### First Party How-To
1. Clone the pluigins repo
1. Follow the structure of the other plugins, implementing the plugin interface as required
1. Make a PR back to this repo!

### Third Party How-To
1. Clone [the third party template](https://github.com/Significant-Gravitas/Auto-GPT-Plugin-Template)
1. Follow the instructions in the [third party template readme](https://github.com/Significant-Gravitas/Auto-GPT-Plugin-Template)

## Get Help

Visit [discord](https://discord.gg/autogpt) server for more information.
