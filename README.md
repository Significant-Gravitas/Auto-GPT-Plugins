<<<<<<< HEAD
# Auto-GPT Email Plugin: Revolutionize Your Email Management with Auto-GPT 🚀

The Auto-GPT Email Plugin is an innovative and powerful plugin for the groundbreaking base software, Auto-GPT. Harnessing the capabilities of the latest Auto-GPT architecture, Auto-GPT aims to autonomously achieve any goal you set, pushing the boundaries of what is possible with artificial intelligence. This email plugin takes Auto-GPT to the next level by enabling it to send and read emails, opening up a world of exciting use cases.

[![GitHub Repo stars](https://img.shields.io/github/stars/riensen/Auto-GPT-Email-Plugin?style=social)](https://github.com/riensen/Auto-GPT-Email-Plugin/stargazers)
[![Twitter Follow](https://img.shields.io/twitter/follow/riensen?style=social)](https://twitter.com/riensen)


<img width="1063" alt="auto-gpt-email-plugin" src="https://user-images.githubusercontent.com/3340218/233331404-fd663c98-5065-4aa5-8cfb-12ce3ed261d0.png">

<img width="1011" alt="gmail-view-auto-gpt-email-plugin" src="https://user-images.githubusercontent.com/3340218/233331422-c5afe433-d4ad-48e0-a0e4-2783cc5f842b.png">

## 🌟 Key Features

- 📬 **Read Emails:** Effortlessly manage your inbox with Auto-GPT's email reading capabilities, ensuring you never miss important information.
- 📤 **Auto-Compose and Send Emails**: Auto-GPT crafts personalized, context-aware emails using its advanced language model capabilities, saving you time and effort.
- 📝 **Save Emails to Drafts Folder:** Gain more control by letting Auto-GPT create email drafts that you can review and edit before sending, ensuring your messages are fine-tuned to your preferences.
- 📎 **Send Emails with Attachments:** Effortlessly send emails with attachments, making your communication richer and more comprehensive.
- 🛡️ **Custom Email Signature:** Personalize your emails with a custom Auto-GPT signature, adding a touch of automation to every message sent by Auto-GPT.
- 🎯 **Auto-Reply and Answer Questions:** Streamline your email responses by letting Auto-GPT intelligently read, analyze, and reply to incoming messages with accurate answers.
- 🔌 **Seamless Integration with Auto-GPT:** Enjoy easy setup and integration with the base Auto-GPT software, opening up a world of powerful automation possibilities.

Unlock the full potential of your email management with the Auto-GPT Email Plugin and revolutionize your email experience today! 🚀

## 🔧 Installation

Follow these steps to configure the Auto-GPT Email Plugin:

### 1. Clone the Auto-GPT-Email-Plugin repository
Clone this repository and navigate to the `Auto-GPT-Email-Plugin` folder in your terminal:

```bash
git clone https://github.com/riensen/Auto-GPT-Email-Plugin.git
```

### 2. Install required dependencies
Execute the following command to install the necessary dependencies:

```bash
pip install -r requirements.txt
```

### 3. Package the plugin as a Zip file
Compress the `Auto-GPT-Email-Plugin` folder or [download the repository as a zip file](https://github.com/riensen/Auto-GPT-Email-Plugin/archive/refs/heads/master.zip).

### 4. Install Auto-GPT
If you haven't already, clone the [Auto-GPT](https://github.com/Significant-Gravitas/Auto-GPT) repository, follow its installation instructions, and navigate to the `Auto-GPT` folder.

### 5. Copy the Zip file into the Auto-GPT Plugin folder
Transfer the zip file from step 3 into the `plugins` subfolder within the `Auto-GPT` repo.

### 6. Locate the `.env.template` file
Find the file named `.env.template` in the main `/Auto-GPT` folder.

### 7. Create and rename a copy of the file
Duplicate the `.env.template` file and rename the copy to `.env` inside the `/Auto-GPT` folder.

### 8. Edit the `.env` file
Open the `.env` file in a text editor. Note: Files starting with a dot might be hidden by your operating system.

### 9. Add email configuration settings
Append the following configuration settings to the end of the file:

```ini
################################################################################
### EMAIL (SMTP / IMAP)
################################################################################

EMAIL_ADDRESS=
EMAIL_PASSWORD=
EMAIL_SMTP_HOST=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_IMAP_SERVER=imap.gmail.com

#Optional Settings
EMAIL_MARK_AS_SEEN=False
EMAIL_SIGNATURE="This was sent by Auto-GPT"
EMAIL_DRAFT_MODE_WITH_FOLDER=[Gmail]/Drafts
```

1. **Email address and password:**
    - Set `EMAIL_ADDRESS` to your sender email address.
    - Set `EMAIL_PASSWORD` to your password. For Gmail, use an [App Password](https://myaccount.google.com/apppasswords).

2. **Provider-specific settings:**
    - If not using Gmail, adjust `EMAIL_SMTP_HOST`, `EMAIL_IMAP_SERVER`, and `EMAIL_SMTP_PORT` according to your email provider's settings.

3. **Optional settings:**
    - `EMAIL_MARK_AS_SEEN`: By default, processed emails are not marked as `SEEN`. Set to `True` to change this.
    - `EMAIL_SIGNATURE`: By default, no email signature is included. Configure this parameter to add a custom signature to each message sent by Auto-GPT.
    - `EMAIL_DRAFT_MODE_WITH_FOLDER`: Prevents emails from being sent and instead stores them as drafts in the specified IMAP folder. `[Gmail]/Drafts` is the default drafts folder for Gmail.


### 10. Allowlist Plugin
In your `.env` search for `ALLOWLISTED_PLUGINS` and add this Plugin:

```ini
################################################################################
### ALLOWLISTED PLUGINS
################################################################################

#ALLOWLISTED_PLUGINS - Sets the listed plugins that are allowed (Example: plugin1,plugin2,plugin3)
ALLOWLISTED_PLUGINS=AutoGPTEmailPlugin
```

## 🧪 Test the Auto-GPT Email Plugin

Experience the plugin's capabilities by testing it for sending and receiving emails.

### 📤 Test Sending Emails

1. **Configure Auto-GPT:**
   Set up Auto-GPT with the following parameters:
   - Name: `CommunicatorGPT`
   - Role: `Communicate`
   - Goals:
     1. Goal 1: `Send an email to my-email-plugin-test@trash-mail.com to introduce yourself`
     2. Goal 2: `Terminate`

2. **Run Auto-GPT:**
   Launch Auto-GPT, which should use the email plugin to send an email to my-email-plugin-test@trash-mail.com.

3. **Verify the email:**
   Check your outbox to confirm that the email was sent. Visit [trash-mail.com](https://www.trash-mail.com/) and enter your chosen email to ensure the email was received.

4. **Sample email content:**
   Auto-GPT might send the following email:
   ```
   Hello,

   My name is CommunicatorGPT, and I am an LLM. I am writing to introduce myself and to let you know that I will be terminating shortly. Thank you for your time.

   Best regards,
   CommunicatorGPT
   ```

### 📬 Test Receiving Emails and Replying Back

1. **Send a test email:**
   Compose an email with a simple question from a [trash-mail.com](https://www.trash-mail.com/) email address to your configured `EMAIL_ADDRESS` in your `.env` file.

2. **Configure Auto-GPT:**
   Set up Auto-GPT with the following parameters:
   - Name: `CommunicatorGPT`
   - Role: `Communicate`
   - Goals:
     1. Goal 1: `Read my latest emails`
     2. Goal 2: `Send back an email with an answer`
     3. Goal 3: `Terminate`

3. **Run Auto-GPT:**
   Launch Auto-GPT, which should automatically reply to the email with an answer.

### 🎁 Test Sending Emails with Attachment

1. **Send a test email:**
   Compose an email with a simple question from a [trash-mail.com](https://www.trash-mail.com/) email address to your configured `EMAIL_ADDRESS` in your `.env` file.

2. **Place attachment in Auto-GPT workspace folder**
   Insert the attachment intended for sending into the Auto-GPT workspace folder, typically named auto_gpt_workspace, which is located within the cloned [Auto-GPT](https://github.com/Significant-Gravitas/Auto-GPT) Github repository.

3. **Configure Auto-GPT:**
   Set up Auto-GPT with the following parameters:
   - Name: `CommunicatorGPT`
   - Role: `Communicate`
   - Goals:
     1. Goal 1: `Read my latest emails`
     2. Goal 2: `Send back an email with an answer and always attach happy.png`
     3. Goal 3: `Terminate`

4. **Run Auto-GPT:**
   Launch Auto-GPT, which should automatically reply to the email with an answer and the attached file.
=======
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
| Telegram | A smoothly working Telegram bot that gives you all the messages you would normally get through the Terminal. | [Wladastic/Auto-GPT-Telegram-Plugin](https://github.com/Wladastic/Auto-GPT-Telegram-Plugin) |
| MetaTrader | Connect your MetaTrader Account to Auto-GPT. | [isaiahbjork/Auto-GPT-MetaTrader-Plugin](https://github.com/isaiahbjork/Auto-GPT-MetaTrader-Plugin) |
| Google Analytics | Connect your Google Analytics Account to Auto-GPT. | [isaiahbjork/Auto-GPT-Google-Analytics-Plugin](https://github.com/isaiahbjork/Auto-GPT-Google-Analytics-Plugin)
| YouTube   | Various YouTube features including downloading and understanding | [jpetzke/AutoGPT-YouTube](https://github.com/jpetzke/AutoGPT-YouTube)

## Configuration

For interactionless use, set `ALLOWLISTED_PLUGINS=example-plugin1,example-plugin2,etc` in your `.env` file.

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
>>>>>>> upstream/master
