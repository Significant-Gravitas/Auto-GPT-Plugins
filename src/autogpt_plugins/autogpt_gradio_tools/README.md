# freddyaboulton/autogpt-gradio-tools 🤝

A plugin giving AutoGPT access to [Gradio](https://github.com/gradio-app/gradio) spaces running on
the [huggingface hub](https://huggingface.co/spaces) and elsewhere!

Integration powered by [gradio-tools](https://github.com/freddyaboulton/gradio-tools)

gradio-tools comes with a set of pre-built tools but it is easy to add new tools. 

All contributions to `gradio-tools` and this plugin are welcome!

## Features

Each tool specified via the env file will add a command that gives AutoGPT
the ability to call that gradio app programmatically and get its prediciton. 

For example, an LLM could use a Gradio tool to transcribe a voice recording it finds online and then summarize it for you. Or it could use a different Gradio tool to apply OCR to a document on your Google Drive and then answer questions about it.

## Installation

1. Download this repository, and save it as `autogpt-gradiot-ools.zip`
2. Place the `.zip` file in the plugins directory of your AutoGPT install
3. Add your twitter API information to the `.env` file within AutoGPT:

```
################################################################################
### GRADIO-TOOLS
################################################################################

# Consumer Keys are also known as API keys on the dev portal

AUTOGPT_GRADIO_TOOLS=StableDiffusion,ImageCaptioner
GRADIO_TOOLS_HF_TOKEN=<Optional hs token to clone spaces and avoid rate limits>
```

