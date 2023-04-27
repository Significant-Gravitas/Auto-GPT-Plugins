# Auto-GPT Allow Unzipped Plugins - a dev utility 🔧

This utility enables faster, on-the-fly plugin testing by allowing unzipped plugins to work. 

Auto-GPT requires zipped plugins for great security reasons. For some developers, zipping up plugins during the dev/test cycle slows things down. 

This tool acts as a proxy between Auto-GPT's plugin API and your unzipped plugins.

⚠️💀 **WARNING** 💀⚠️:
1. Do not use this tool with plugins you are not developing.
2. Only use this tool if your development workflow requires it.
3. Review the code of any plugin you use thoroughly, as plugins can execute any Python code, potentially leading to malicious activities, such as stealing your API keys.

## 🔧 Installation

Follow these steps to configure the Auto-GPT Email Plugin:

### 1. Follow Auto-GPT-Plugins Installation Instructions
Follow the instructions as per the [Auto-GPT-Plugins/README.md](https://github.com/Significant-Gravitas/Auto-GPT-Plugins/blob/master/README.md)

### 2. Locate the `.env.template` file
Find the file named `.env.template` in the main `/Auto-GPT` folder.

### 3. Create and rename a copy of the file
Duplicate the `.env.template` file and rename the copy to `.env` inside the `/Auto-GPT` folder.

### 4. Edit the `.env` file
Open the `.env` file in a text editor. Note: Files starting with a dot might be hidden by your operating system.

### 5. Allowlist Plugin
In your `.env` search for `ALLOWLISTED_PLUGINS` and add this Plugin:

```ini
################################################################################
### ALLOWLISTED PLUGINS
################################################################################

#ALLOWLISTED_PLUGINS - Sets the listed plugins that are allowed (Example: plugin1,plugin2,plugin3)
ALLOWLISTED_PLUGINS=AutoGPTAllowUnzippedPlugins
```

## Usage

1. Once installed, this plugin allows Auto-GPT to call any plugin in the "Auto-GPT/plugins/" directory even if they're not zipped up.
2. Place your plugins in the "Auto-GPT/plugins/" folder, as you normally would, except that you do not have to zip them up.

## Limitations

1. The plugins will not show up in Auto-GPT's plugin list, but plugin methods will be called.
2. Currently, the plugin does not support the following methods.
- chat_completion
- on_planning