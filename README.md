# Auto-GPT-Plugins

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

| Plugin       | Description     |
|--------------|-----------|
| Twitter      | AutoGPT is capable of retrieving Twitter posts and other related content by accessing the Twitter platform.|

## Third party plugins:
Some third-party plugins have been created by contributors that are not included in this repository. For more information about these plugins, please visit their respective GitHub pages.

| Plugin       | Description     | Repository |
|--------------|-----------------|-------------|
| SystemInformation      | This plugin adds an extra line to the prompt, serving as a hint for the AI to use shell commands likely supported by the current system. By incorporating this plugin, you can ensure that the AI model provides more accurate and system-specific shell commands, improving its overall performance and usefulness. | [hdkiller/Auto-GPT-SystemInfo](https://github.com/hdkiller/Auto-GPT-SystemInfo) |
| Notion      | Notion plugin for Auto-GPT.  | [doutv/Auto-GPT-Notion](https://github.com/doutv/Auto-GPT-Notion) |
| Email-Plugin | Revolutionize Your Email Management with Auto-GPT | [riensen/Auto-GPT-Email-Plugin](https://github.com/riensen/Auto-GPT-Email-Plugin)

## Get Help

Visit [discord](https://discord.gg/autogpt) server for more information.

