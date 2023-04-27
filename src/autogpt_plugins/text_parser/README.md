# Auto-GPT Text Parser Plugin

The Auto-GPT Text Parser Plugin supports reading text from several types of files directly without converting them to .txt files.

## ⭐ Key Features:
- Text Parsing: Parse plain text from many types of files.

## 📄 Available File Extension
- `.csv`
- `.pdf`
- `.docx`
- `.json`
- `.xml`
- `.yaml`
- `.html`
- `.md`
- `.tex`
- `.epub`

## ⚙️ Installation:
1. Download the Auto-GPT-Plugin repository as a ZIP file.
2. Copy the ZIP file into the "plugins" folder of your Auto-GPT project.

## 🔍 How to use
1. <b> Check files </b>: 
    - Move your files to be parsed to `../auto_gpt_workspace` directory.

2. <b> Configure Auto-GPT </b>:
    - Set up Auto-GPT with the following goal.
    - Goals:
        - Goal 1: Parse text from 'sample.pdf' file
        - Goal 2: Do whatever you want.

Then, Auto-GPT's `NEXT ACTION` would be like

```
NEXT ACTION:  COMMAND = parse_text ARGUMENTS = {'filename': '/Users/../Auto-GPT/autogpt/auto_gpt_workspace/sample.pdf'}
```
