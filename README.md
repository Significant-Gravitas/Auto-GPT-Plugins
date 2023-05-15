# Auto-GPT-Plugins

> ⚠️💀 **WARNING** 💀⚠️:
> Always examine the code of any plugin you use thoroughly, as plugins can execute any Python code, leading to potential malicious activities such as stealing your API keys.

> ⚙️ **WORK IN PROGRESS** ⚙️:
> The plugin API is still being refined. If you are developing a plugin, expect changes in the upcoming versions.

## Installation

**_⚠️This is a work in progress⚠️_**

Here are the steps to configure Auto-GPT Plugins:

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

## Plugins

> For interactionless use, set `ALLOWLISTED_PLUGINS=example-plugin1,example-plugin2,example-plugin3` in your `.env`

There are two categories of plugins: **first party** and **third party**. First-party plugins are included in this repo and are installed by default when the plugin platform is installed. Third-party plugins need to be added individually. Use first-party plugins for widely-used plugins, and third-party for your specific needs. **You can view all the plugins and their contributors on this [directory](https://autoplugins.vercel.app/).**

If you've built a plugin and it's not listed in the directory, you can make a PR to this [repo](https://github.com/dylanintech/autoplugins) by adding your plugin to the `data` array in `plugins.tsx`.

You can also view the plugins here:

[//]: # (First-party plugins table)
<!-- Table of first-party plugins goes here -->

[//]: # (Third-party plugins table)
<!-- Table of third-party plugins goes here -->

Some third-party plugins have been created by contributors that are not included in this repository. For more information about these plugins, please visit their respective GitHub pages.

## Configuration

For interactionless use, set:

`ALLOWLISTED_PLUGINS=example-plugin1,example-plugin2,etc` in your `.env` file to allow plugins to load without prompting.
`DENYLISTED_PLUGINS=example-plugin1,example-plugin2,etc` in your `.env` file to block plugins from loading without prompting.

## Creating a Plugin

Creating a plugin is a rewarding experience! You can choose between first-party or third-party plugins. First-party plugins are included in this repo and are installed by default along with other plugins when the plugin platform is installed. Third-party plugins need to be added individually. Use first-party plugins for plugins you expect others to use and want, and third-party for things specific to you.

### First Party Plugins How-To

1. Clone the plugins repository.
2. Follow the structure of the other plugins, implementing the plugin interface as required.
3. Write your tests.
4. Add your name to the [codeowners](.github/CODEOWNERS) file.
5. Add your plugin to the [Readme](README.md).
6. Submit a pull request back to this repository!

### Third Party Plugins How-To

1. Clone [the third party template](https://github.com/Significant-Gravitas/Auto-GPT-Plugin-Template).
2. Follow the instructions in the [third party template readme](https://github.com/Significant-Gravitas/Auto-GPT-Plugin-Template).

### Migrating Third Party to First Party

We appreciate your contribution of a plugin to the project!

1. Clone this repository.
2. Make a folder for your plugin under `src/autogpt_plugins`. Use a simple descriptive name such as `notion`, `twitter`, or `web_ui`.
3. Add the files from your third-party plugin located at `src/auto_gpt_plugin_template` into the folder you created.
4. Include your README from your third-party plugin in the folder you created.
5. Add your plugin to the root README with a description and a link to your plugin-specific README.
6. Add your plugin's Python package requirements to `requirements.txt`.
7. Add tests to get your plugin to 80% code coverage.
8. Add your name to the [codeowners](.github/CODEOWNERS) file.
9. Add your plugin to the [Readme](README.md).
10. Submit a pull request back to this repository!

## Get Help

For more information, visit the [discord](https://discord.gg/autogpt) server.
