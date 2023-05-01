# Bing AI Plugin

The Bing AI Plugin enables Auto-GPT to use Bing AI to research information, ask questions, get advice, and more.

## Key Features:
- Bing AI already implemented researching information, so implementing this plugin will almost entirely negate the need to browse websites and the current implementation of researching information.
- Allows Auto-GPT to consult Bing AI.
- Allows Auto-GPT to be able to use GPT-4 as Bing AI is based on GPT-4.
- Brings GPT-4 functionality to those without GPT-4 API access.

## Getting Authentication (Required):
- Install the cookie editor extension for [Chrome](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) or [Firefox](https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/)
- Go to `bing.com`
- Open the extension
- Click "Export" on the bottom right, then "Export as JSON" (This saves your cookies to clipboard)
- Paste your cookies into a file `cookies.json`

## Installation

Follow these steps to configure the Auto-GPT Email Plugin:

### 1. Follow Auto-GPT-Plugins Installation Instructions
Follow the instructions as per the [Auto-GPT-Plugins/README.md](https://github.com/Significant-Gravitas/Auto-GPT-Plugins/blob/master/README.md)

### 2. Locate the `.env.template` file
Find the file named `.env.template` in the main `/Auto-GPT` folder.

### 3. Create and rename a copy of the file
Duplicate the `.env.template` file and rename the copy to `.env` inside the `/Auto-GPT` folder.

### 4. Edit the `.env` file
Open the `.env` file in a text editor. Note: Files starting with a dot might be hidden by your operating system.

### 5. Add email configuration settings
Append the following configuration settings to the end of the file:

```ini
################################################################################
### BINGAI
################################################################################

BING_AI_COOKIES_PATH=
```

## AutoGPT Configuration
Set `ALLOWLISTED_PLUGINS=BingAI,example-plugin1,example-plugin2,etc` in your AutoGPT `.env` file.