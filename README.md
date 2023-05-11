# Auto-GPT-Plugins

> ⚠️💀 **WARNING** 💀⚠️:
> Review the code of any plugin you use thoroughly, as plugins can execute any Python code, potentially leading to malicious activities, such as stealing your API keys.

> ⚙️ **WORK IN PROGRESS** ⚙️:
> The plugin api is not yet stabilized. If you are coding a plugin, expect it to change in the next few versions.

## Installation

**_⚠️This is a work in progress⚠️_**

Follow these steps to configure the Auto-GPT Plugins:

1. **Install Auto-GPT**

   If you haven't already, follow the installation instructions provided by [Auto-GPT](https://github.com/Significant-Gravitas/Auto-GPT) to install it.

1. **Run the following to pull the plugins folder down from the `root` of `Auto-GPT` directory**

    To download it directly from your Auto-GPT directory, you can run this command on Linux or MacOS:

    ```bash
    curl -L -o ./plugins/Auto-GPT-Plugins.zip https://github.com/Significant-Gravitas/Auto-GPT-Plugins/archive/refs/heads/master.zip
    ```

    In PowerShell:

    ```pwsh
    Invoke-WebRequest -Uri "https://github.com/Significant-Gravitas/Auto-GPT-Plugins/archive/refs/heads/master.zip"     -OutFile "./plugins/Auto-GPT-Plugins.zip"
    ```

1. **Run the dependency install script for plugins**
    You can run it with either:
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

## Plugins

> For interactionless use, set `ALLOWLISTED_PLUGINS=example-plugin1,example-plugin2,example-plugin3` in your `.env`

There are two kinds of plugins: **first party** and **third party**. First-party plugins are included in this repo and are installed by default along with other plugins when the plugin platform is installed. Third-party plugins need to be added individually. Use first-party plugins for plugins you expect others to use and want, and third-party for things specific to you. You can see all the plugins and their contributors on this [directory](https://autoplugins.vercel.app/).

If you built a plugin and it's not on the directory yet simply make a PR to this [repo](https://github.com/dylanintech/autoplugins) by adding your plugin to the `data` array in `plugins.tsx`.

## Configuration

For interactionless use, set:

`ALLOWLISTED_PLUGINS=example-plugin1,example-plugin2,etc` in your `.env` file to allow plugins to load without prompting.
`DENYLISTED_PLUGINS=example-plugin1,example-plugin2,etc` in your `.env` file to block plugins from loading without prompting.

## Making a plugin

Creating a plugin is a rewarding experience! You can choose between first-party or third-party plugins. First-party plugins are included in this repo and are installed by default along with other plugins when the plugin platform is installed. Third-party plugins need to be added individually. Use first-party plugins for plugins you expect others to use and want, and third-party for things specific to you.

### First Party How-To

1. Clone the plugins repo
1. Follow the structure of the other plugins, implementing the plugin interface as required
1. Write your tests
1. Add your name to the [codeowners](.github/CODEOWNERS) file
1. Add your plugin to the [Readme](README.md)
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
1. Add your name to the [codeowners](.github/CODEOWNERS) file
1. Add your plugin to the [Readme](README.md)
1. Make a PR back to this repo!

## Get Help

Visit the [discord](https://discord.gg/autogpt) server for more information.
