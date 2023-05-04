# Random Values Plugin

The Random Values plugin will enable AutoGPT to generate various random assorted things like numbers and strings.

## Key Features:
- make_uuids generates 1 or more UUIDs (128-bit label)
- generate_string generates 1 or more alphanumeric strings of at least 2 characters in length
- generate_password generates 1 or more passwords of 6 or more characters using letters, numbers and punctuation
- generate_placeholder_text generates 1 or more sentences of lorem ipsum text
- random_number draws 1 or more random numbers between min and max

## Installation:
As part of the AutoGPT plugins package, follow the [installation instructions](https://github.com/Significant-Gravitas/Auto-GPT-Plugins) on the Auto-GPT-Plugins GitHub reporistory README page.

## AutoGPT Configuration

Set `ALLOWLISTED_PLUGINS=autogpt-random-values,example-plugin1,example-plugin2,etc` in your AutoGPT `.env` file.
