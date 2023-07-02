# Auto-GPT-Plugins

> ⚠️💀 **WARNING** 💀⚠️:
> Always examine the code of any plugin you use thoroughly, as plugins can execute any Python code, leading to potential malicious activities such as stealing your API keys.

> ⚙️ **WORK IN PROGRESS** ⚙️:
> The plugin API is still being refined. If you are developing a plugin, expect changes in the upcoming versions.

## New in Auto-GPT 0.4.1
- Unzipped plugins are now supported! You can now clone or download plugins directly from GitHub and place them in the `plugins` directory without zipping, as long as they are in the correct (NEW) format.
- Plugins settings have been moved out of the `.env` file to a new `plugins_config.yaml` file in the root directory of Auto-GPT.
- `ALLOWLISTED_PLUGINS` and `DENYLISTED_PLUGINS` `.env` settings are deprecated and will be removed in a future release.
- Plugins must now be explicitly enabled in plugins. See the [installation](#installation) section for more details.
- The plugin format has changed. For now the old zip format is still supported, but will be removed in a future release. See the [plugin format](#plugin-format) section for more details.

### Note: The Auto-GPT-Plugins repo must still be Zipped

> The core Auto-GPT Plugins are still in the old format, and will need to be zipped as shown in the instructions below. **THEY WILL NOT WORK UNZIPPED**. This will be fixed in a future release.

## Installation

**_⚠️This is a work in progress⚠️_**

Here are the steps to configure Auto-GPT Plugins. 

1. **Install Auto-GPT**

   If you haven't done so, follow the installation instructions given by [Auto-GPT](https://github.com/Significant-Gravitas/Auto-GPT) to install it.

1. **Download the plugins folder from the `root` of `Auto-GPT` directory**

    To download it directly from your Auto-GPT directory, you can run this command on Linux or MacOS:

    ```bash
    curl -L -o ./plugins/Auto-GPT-Plugins.zip https://github.com/Significant-Gravitas/Auto-GPT-Plugins/archive/refs/heads/master.zip
    ```

    Or in PowerShell:

    ```pwsh
    Invoke-WebRequest -Uri "https://github.com/Significant-Gravitas/Auto-GPT-Plugins/archive/refs/heads/master.zip"     -OutFile "./plugins/Auto-GPT-Plugins.zip"
    ```

1. **Execute the dependency install script for plugins**

    This can be run via:

    Linux or MacOS:

    ```bash
    ./run.sh --install-plugin-deps
    ```

   Windows:

    ```pwsh
   .\run.bat --install-plugin-deps
    ```

    Or directly via the CLI:

    ```bash
    python -m autogpt --install-plugin-deps
    ````

1. **Enable the plugins** 

    To activate a plugin, the user should create or edit the `plugins_config.yaml` file located in the root directory of Auto-GPT. All plugin options can be configured in this file. 
    
    For example, if the `astro` plugin needs to be enabled, the following line should be added to the `plugins_config.yaml` file:
    ```yaml
    AutoGPTSpacePlugin:
        config: {}
        enabled: true
    ```

## Plugins

There are two categories of plugins: **first party** and **third party**.

 **First-party plugins** are a curated list of widely-used plugins, and are included in this repo. They and are installed by default when the plugin platform is installed. See the [First Party Plugins](#first-party-plugins) section below for a comprehensive list.

 **Third-party plugins** need to be added individually. They may be useful for your specific needs. See the [Third Party Plugins](#third-party-plugins) section below for a short list of third-party plugins, and for information on how to add your plugin. Note: The Auto-GPT community has developed numerous third-party plugins and this list doesn't include them all. See the [Community-contributed plugins directory](#community-contributed-plugins-directory) section below for a more comprehensive list.

### Community contributed plugins directory

Community member and contributor, **[@dylanintech](https://github.com/dylanintech/)**, maintains a [**growing directory**](https://autoplugins.vercel.app/) of **Auto-GPT plugins and their contributors. To get your plugin listed in that directory, add your info to the `data` array in `plugins.tsx` of [his repo](https://github.com/dylanintech/autoplugins) and submit a PR. 

### First Party Plugins

You can see the first-party plugins below. These are included in this Auto-GPT-Plugins repo and are installed by default when the plugin platform is installed.

| Plugin       | Description     | Location |
|--------------|-----------|--------|
| Astro Info   | This gives Auto-GPT info about astronauts.                                                           | [autogpt_plugins/astro](https://github.com/Significant-Gravitas/Auto-GPT-Plugins/tree/master/src/autogpt_plugins/astro)           |
| API Tools        | This allows Auto-GPT to make API calls of various kinds.                                                           | [autogpt_plugins/api_tools](https://github.com/Significant-Gravitas/Auto-GPT-Plugins/tree/master/src/autogpt_plugins/api_tools)           |
| Baidu Search |  This search plugin integrates Baidu search engines into Auto-GPT. | [autogpt_plugins/baidu_search](https://github.com/Significant-Gravitas/Auto-GPT-Plugins/tree/master/src/autogpt_plugins/baidu_search)|
| Bing Search      | This search plugin integrates Bing search engines into Auto-GPT.                                                  | [autogpt_plugins/bing_search](https://github.com/Significant-Gravitas/Auto-GPT-Plugins/tree/master/src/autogpt_plugins/bing_search)       |
| Bluesky | Enables Auto-GPT to retrieve posts from Bluesky and create new posts. | [autogpt_plugins/bluesky](https://github.com/Significant-Gravitas/Auto-GPT-Plugins/tree/master/src/autogpt_plugins/bluesky)|
| Email            | Revolutionize email management with the Auto-GPT Email Plugin, leveraging AI to automate drafting and intelligent replies. | [autogpt_plugins/email](https://github.com/Significant-Gravitas/Auto-GPT-Plugins/tree/master/src/autogpt_plugins/email)                 |
| News Search      | This search plugin integrates News Articles searches, using the NewsAPI aggregator into Auto-GPT.                 | [autogpt_plugins/news_search](https://github.com/Significant-Gravitas/Auto-GPT-Plugins/tree/master/src/autogpt_plugins/news_search)   |
| Planner          | Simple Task Planner Module for Auto-GPT  | [autogpt_plugins/planner](https://github.com/Significant-Gravitas/Auto-GPT-Plugins/blob/master/src/autogpt_plugins/planner/) |
| Random Values    | Enable Auto-GPT to generate various random numbers and strings.                                                    | [autogpt_plugins/random_values](https://github.com/Significant-Gravitas/Auto-GPT-Plugins/tree/master/src/autogpt_plugins/random_values) |
| SceneX           | Explore image storytelling beyond pixels with the Auto-GPT SceneX Plugin.                                        | [autogpt_plugins/scenex](https://github.com/Significant-Gravitas/Auto-GPT-Plugins/tree/master/src/autogpt_plugins/scenex)               |
| Telegram |  A smoothly working Telegram bot that gives you all the messages you would normally get through the Terminal. | [autogpt_plugins/telegram](https://github.com/Significant-Gravitas/Auto-GPT-Plugins/tree/master/src/autogpt_plugins/telegram) |
| Twitter          | Auto-GPT is capable of retrieving Twitter posts and other related content by accessing the Twitter platform via the v1.1 API using Tweepy.               | [autogpt_plugins/twitter](https://github.com/Significant-Gravitas/Auto-GPT-Plugins/tree/master/src/autogpt_plugins/twitter)           |
| Wikipedia Search | This allows Auto-GPT to use Wikipedia directly.                                                                    | [autogpt_plugins/wikipedia_search](https://github.com/Significant-Gravitas/Auto-GPT-Plugins/tree/master/src/autogpt_plugins/wikipedia_search) |
| WolframAlpha Search | This allows AutoGPT to use WolframAlpha directly.                                                                                         | [autogpt_plugins/wolframalpha_search](https://github.com/Significant-Gravitas/Auto-GPT-Plugins/tree/master/src/autogpt_plugins/wolframalpha_search)|


### Third Party Plugins

Third-party plugins are created by contributors and are not included in this repository. For more information about these plugins, please visit their respective GitHub pages.

Here is a non-comprehensive list of third-party plugins. If you have a plugin you'd like to add to this list, please submit a PR.

| Plugin       | Description     | Repository |
|--------------|-----------------|-------------|
| Alpaca-Trading | Trade stocks and crypto, paper or live with Auto-GPT | [danikhan632/Auto-GPT-AlpacaTrader-Plugin](https://github.com/danikhan632/Auto-GPT-AlpacaTrader-Plugin)|
| AutoGPT User Input Request | Allow Auto-GPT to specifically request user input in continous mode | [HFrovinJensen/Auto-GPT-User-Input-Plugin](https://github.com/HFrovinJensen/Auto-GPT-User-Input-Plugin)|
| BingAI | Enable Auto-GPT to fetch information via BingAI, saving time, API requests while maintaining accuracy. This does not remove the need for OpenAI API keys | [gravelBridge/AutoGPT-BingAI](https://github.com/gravelBridge/AutoGPT-BingAI)|
| Crypto | Trade crypto with Auto-GPT | [isaiahbjork/Auto-GPT-Crypto-Plugin](https://github.com/isaiahbjork/Auto-GPT-Crypto-Plugin)|
| Discord | Interact with your Auto-GPT instance through Discord | [gravelBridge/AutoGPT-Discord](https://github.com/gravelBridge/AutoGPT-Discord)|
| Dolly AutoGPT Cloner | A way to compose & run multiple Auto-GPT processes that cooperate, till core has multi-agent support | [pr-0f3t/Auto-GPT-Dolly-Plugin](https://github.com/pr-0f3t/Auto-GPT-Dolly-Plugin)|
| Google Analytics | Connect your Google Analytics Account to Auto-GPT. | [isaiahbjork/Auto-GPT-Google-Analytics-Plugin](https://github.com/isaiahbjork/Auto-GPT-Google-Analytics-Plugin)|
| IFTTT webhooks | This plugin allows you to easily integrate IFTTT connectivity using Maker | [AntonioCiolino/AutoGPT-IFTTT](https://github.com/AntonioCiolino/AutoGPT-IFTTT)|
| iMessage | Send and Get iMessages using Auto-GPT | [danikhan632/Auto-GPT-Messages-Plugin](https://github.com/danikhan632/Auto-GPT-Messages-Plugin)|
| Instagram | Instagram access | [jpetzke/AutoGPT-Instagram](https://github.com/jpetzke/AutoGPT-Instagram)|
| Mastodon  | Simple Mastodon plugin to send toots through a Mastodon account | [ppetermann/AutoGPTMastodonPlugin](https://github.com/ppetermann/AutoGPTMastodonPlugin)|
| MetaTrader | Connect your MetaTrader Account to Auto-GPT. | [isaiahbjork/Auto-GPT-MetaTrader-Plugin](https://github.com/isaiahbjork/Auto-GPT-MetaTrader-Plugin) |
| Notion      | Notion plugin for Auto-GPT.  | [doutv/Auto-GPT-Notion](https://github.com/doutv/Auto-GPT-Notion) |
| Slack | This plugin allows to receive commands and send messages to slack channels | [adithya77/Auto-GPT-slack-plugin](https://github.com/adithya77/Auto-GPT-slack-plugin)
| Spoonacular | Find recipe insiprations using Auto-GPT | [minfenglu/Auto-GPT-Spoonacular-Plugin](https://github.com/minfenglu/Auto-GPT-Spoonacular-Plugin)
| System Information      | This plugin adds an extra line to the prompt, serving as a hint for the AI to use shell commands likely supported by the current system. By incorporating this plugin, you can ensure that the AI model provides more accurate and system-specific shell commands, improving its overall performance and usefulness. | [hdkiller/Auto-GPT-SystemInfo](https://github.com/hdkiller/Auto-GPT-SystemInfo) |
| TiDB Serverless   | Connect your TiDB Serverless database to Auto-GPT, enable get query results from database | [pingcap/Auto-GPT-TiDB-Serverless-Plugin](https://github.com/pingcap/Auto-GPT-TiDB-Serverless-Plugin)
| Todoist-Plugin | Allow Auto-GPT to programatically interact with yor Todoist to create, update, and manage your Todoist | [danikhan632/Auto-GPT-Todoist-Plugin](https://github.com/danikhan632/Auto-GPT-Todoist-Plugin) |
| Weather | A simple weather plugin wrapping around python-weather | [ppetermann/Auto-GPT-WeatherPlugin](https://github.com/ppetermann/Auto-GPT-WeatherPlugin) |
| Web-Interaction | Enable Auto-GPT to fully interact with websites! Allows Auto-GPT to click elements, input text, and scroll | [gravelBridge/AutoGPT-Web-Interaction](https://github.com/gravelBridge/AutoGPT-Web-Interaction)|
| WolframAlpha | Access to WolframAlpha to do math and get accurate information | [gravelBridge/AutoGPT-WolframAlpha](https://github.com/gravelBridge/AutoGPT-WolframAlpha)|
| YouTube   | Various YouTube features including downloading and understanding | [jpetzke/AutoGPT-YouTube](https://github.com/jpetzke/AutoGPT-YouTube) |
| Zapier webhooks | This plugin allows you to easily integrate Zapier connectivity | [AntonioCiolino/AutoGPT-Zapier](https://github.com/AntonioCiolino/AutoGPT-Zapier)|
| Project Management | Streamline your Project Management with ease: Jira, Trello, and Google Calendar Made Effortless| [minfenglu/AutoGPT-PM-Plugin](https://github.com/minfenglu/AutoGPT-PM-Plugin)|
| RabbitMQ | This plugin allows you to communicate with your Auto-GPT instance via microservice.| [tomtom94/AutoGPT-RabbitMQ](https://github.com/tomtom94/AutoGPT-RabbitMQ)|

## Configuration

Plugins must be enabled in `plugins_config.yaml`. 

If you still have `ALLOWLISTED_PLUGINS` and `DENYLISTED_PLUGINS` in your `.env` file, Auto-GPT will use them to create the `plugins_config.yaml` file the first time. 

This file contains a list of plugins to load. The format is as follows:

```yaml
plugin_a:
  config:
    api_key: my-api-key
  enabled: false
PluginB:
  config: {}
  enabled: true

```

The various sections are as follows:

- key: The name of the plugin. E.g. `plugin_a` or `PluginB`.

    This is used to load the plugin. It's format depends on whether the plugin is zipped or unzipped.
    
    **For zipped plugins**, the key must be the name of the plugin **class**. For example, the `weather` plugin in this repository would `WeatherPlugin`, and in the example above, `PluginB` is most likely a zipped plugin.

    **For unzipped plugins**, the key must be the name of the plugin **directory**. For example, in the example above, the `plugin_a` directory would be loaded as a plugin.

- config: The configuration for the plugin. 

    This is passed to the plugin when it is loaded. The format of this field depends on the plugin. This field is optional. Use `{}` if you do not need to pass any configuration to the plugin.

    Note that `plugins_config.yaml` file is only used by Auto-GPT to decide whether to load a plugin. For specific plugin settings, please refer to the documentation provided for each plugin. Plugin developers may still rely on`.env` for other plugin specific settings. We encourage developers to migrate their settings to the `config` field in the new `plugins_config.yaml` file.

- enabled: Determines whether the plugin is loaded. 

## Creating a Plugin

Creating a plugin is a rewarding experience! You can choose between first-party or third-party plugins. First-party plugins are included in this repo and are installed by default along with other plugins when the plugin platform is installed. Third-party plugins need to be added individually. Use first-party plugins for plugins you expect others to use and want, and third-party for things specific to you.

## Plugin Format

Plugins must follow a specific structure in order to be found and loaded successfully. The structure depends on whether a plugin is zipped or unzipped.

Zipped plugins must subclasses `AutoGPTPluginTemplate`(https://github.com/Significant-Gravitas/Auto-GPT-Plugin-Template), and implement all the methods defined in AutoGPTPluginTemplate.

Unzipped plugins can also subclass `AutoGPTPluginTemplate`, but it is not required. They can implement only the methods they need. However, the name of the plugin's directory is used to load the plugin, so it must be unique within AutoGPT's `plugins` directory.

### First Party Plugins How-To

1. Clone this plugins repo
1. Follow the structure of the other plugins, implementing the plugin interface as required
1. Write your tests
1. Add your name to the [codeowners](.github/CODEOWNERS) file
1. Add your plugin to the [Readme](README.md)
1. Add your plugin to the [autogpt-package](https://github.com/kurtosis-tech/autogpt-package/blob/main/plugins.star). You can copy the line of any of the standard plugins and just add another entry in the dictionary. Raise a PR & get it merged
1. Add your plugin to the [plugin installation integration test](.github/workflows/test-plugin-installation.yml)
1. Make a PR back to this repo!

### Third Party Plugins How-To

1. Clone [the third party template](https://github.com/Significant-Gravitas/Auto-GPT-Plugin-Template).
1. Follow the instructions in the [third party template readme](https://github.com/Significant-Gravitas/Auto-GPT-Plugin-Template).

### Migrating Third Party to First Party

We appreciate your contribution of a plugin to the project!

1. Clone this repository.
1. Make a folder for your plugin under `src/autogpt_plugins`. Use a simple descriptive name such as `notion`, `twitter`, or `web_ui`.
1. Add the files from your third-party plugin located at `src/auto_gpt_plugin_template` into the folder you created.
1. Include your README from your third-party plugin in the folder you created.
1. Add your plugin to the root README with a description and a link to your plugin-specific README.
1. Add your plugin's Python package requirements to `requirements.txt`.
1. Add tests to get your plugin to 80% code coverage.
1. Add your name to the [codeowners](.github/CODEOWNERS) file.
1. Add your plugin to the [Readme](README.md).
1. Submit a pull request back to this repository!

## Get Help

For more information, visit the [discord](https://discord.gg/autogpt) server.
