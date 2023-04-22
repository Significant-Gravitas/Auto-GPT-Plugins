# Auto-GPT-Plugins

> ⚠️💀 **WARNING** 💀⚠️:
> Review the code of any plugin you use thoroughly, as plugins can execute any Python code, potentially leading to malicious activities, such as stealing your API keys.

## Installation

**_⚠️This is a work in progress⚠️_**

Follow these steps to configure the Auto-GPT Plugins:

1. **Install Auto-GPT**

   If you haven't already, create a folder `Significant-Gravitas` and clone the [Auto-GPT](https://github.com/Significant-Gravitas/Auto-GPT) repository into the folder. Follow the installation instructions provided by [Auto-GPT](https://github.com/Significant-Gravitas/Auto-GPT).

1. **Clone the Auto-GPT-Plugins repository**

   Clone this repository into the `Significant-Gravitas` folder as well:
   ```
   git clone https://github.com/Significant-Gravitas/Auto-GPT-Plugins.git
   ```
   You should now have two folders in your `Significant-Gravitas` folder: `Auto-GPT` and `Auto-GPT-Plugins`.

1. **Install required dependencies**

   Navigate to the Auto-GPT-Plugins folder in your terminal and execute the following command to install the necessary dependencies:

   - For Command Prompt:
   ```
   pip install -r requirements.txt
   ```
   
   - For PowerShell:
   ```
   pip install -r .\requirements.txt
   ```

1. **Package the plugin as a Zip file**

   Execute the following command to compress the Auto-GPT-Plugins folder and place the archive into the `Auto-GPT/plugins` folder:

   - For Command Prompt:
   ```
   zip -ru ../Auto-GPT/plugins/Auto-GPT-Plugins.zip
   ```
   
   - For PowerShell:
   ```
   Compress-Archive -Path .\* -DestinationPath ..\Auto-GPT\plugins\Auto-GPT-Plugins.zip -Force
   ```

   Alternatively, you can manually zip the `Auto-GPT-Plugins` folder, rename it to Auto-GPT-Plugins.zip, and then paste the zip file into the `Auto-GPT/plugins/` directory.


## Plugins in the repository

For interactionless use, set `ALLOWLISTED_PLUGINS=example-plugin1,example-plugin2,example-plugin3` in your `.env`

| Plugin       | Description     | Location |
|--------------|-----------|--------|
| Twitter      | AutoGPT is capable of retrieving Twitter posts and other related content by accessing the Twitter platform via the v1.1 API using Tweepy.| [autogpt_plugins/twitter](https://github.com/Significant-Gravitas/Auto-GPT-Plugins/tree/master/src/autogpt_plugins/twitter)
| Email | Revolutionize email management with the Auto-GPT Email Plugin, leveraging AI to automate drafting and intelligent replies. | [autogpt_plugins/email](https://github.com/Significant-Gravitas/Auto-GPT-Plugins/tree/master/src/autogpt_plugins/email)

Some third-party plugins have been created by contributors that are not included in this repository. For more information about these plugins, please visit their respective GitHub pages.

| Plugin       | Description     | Repository |
|--------------|-----------------|-------------|
| System Information      | This plugin adds an extra line to the prompt, serving as a hint for the AI to use shell commands likely supported by the current system. By incorporating this plugin, you can ensure that the AI model provides more accurate and system-specific shell commands, improving its overall performance and usefulness. | [hdkiller/Auto-GPT-SystemInfo](https://github.com/hdkiller/Auto-GPT-SystemInfo) |
| Notion      | Notion plugin for Auto-GPT.  | [doutv/Auto-GPT-Notion](https://github.com/doutv/Auto-GPT-Notion) |
| Telegram | A smoothly working Telegram bot that gives you all the messages you would normally get through the Terminal. | [Wladastic/Auto-GPT-Telegram-Plugin](https://github.com/Wladastic/Auto-GPT-Telegram-Plugin)

## Configuration

For interactionless use, set `ALLOWLISTED_PLUGINS=example-plugin1,example-plugin2,etc` in your `.env` file.

## Making a plugin

Creating a plugin is a rewarding experience! You can choose between first-party or third-party plugins. First-party plugins are included in this repo and are installed by default along with other plugins when the plugin platform is installed. Third-party plugins need to be added individually. Use first-party plugins for plugins you expect others to use and want, and third-party for things specific to you.

### First Party How-To

1. Clone the plugins repo
1. Follow the structure of the other plugins, implementing the plugin interface as required
1. Write your tests
1. Make a PR back to this repo!

### Third Party How-To

1. Clone [the third party template](https://github.com/Significant-Gravitas/Auto-GPT-Plugin-Template)
1. Follow the instructions in the [third party template readme](https://github.com/Significant-Gravitas/Auto-GPT-Plugin-Template)

### Migrating Third Party to First Party

> Thanks for contributing a plugin to the project!

1. Clone this repo.
1. Make a folder for your plugin under `src/autogpt_plugins`. Name it a simple descriptive name such as `notion`, `twitter`, or `web_ui`.
1. Take the files from your third-party plugin located at `src/auto_gpt_plugin_template` and add them into the folder you created
1. Add your readme from your third-party plugin to the folder you created
1. Add your plugin to the root readme with a description and a link to your plugin-specific readme
1. Add your plugin's Python package requirements to `requirements.txt`
1. Add tests to get your plugin to 80% code coverage

## Get Help

Visit the [discord](https://discord.gg/autogpt) server for more information.
