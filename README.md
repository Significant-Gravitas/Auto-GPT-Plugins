# Auto-GPT Email Plugin: Revolutionize Your Email Management with Auto-GPT
The Auto-GPT Email Plugin is an innovative and powerful plugin for the groundbreaking base software, Auto-GPT. Harnessing the capabilities of the latest Auto-GPT architecture, Auto-GPT aims to autonomously achieve any goal you set, pushing the boundaries of what is possible with artificial intelligence. This email plugin takes Auto-GPT to the next level by enabling it to send and read emails, opening up a world of exciting use cases.

## Key Features:
- **Email Management**: Bid farewell to cluttered inboxes and missed emails. The Auto-GPT Email Plugin empowers Auto-GPT to categorize, prioritize, and manage your emails with unparalleled efficiency. No more manually sifting through hundreds of emails; let AI handle it with ease.

- **Automated Replies**: Whether it's answering inquiries, providing customer support, or acknowledging receipt of important messages, the Auto-GPT Email Plugin allows Auto-GPT to compose and send accurate, context-aware, and human-like email replies that save you time and effort.

- **Email Scheduling**: Plan your communication like never before. The plugin enables Auto-GPT to schedule emails based on your preferences and recipients' availability, ensuring optimal delivery times and increased engagement.

- **Smart Email Summarization**: Don't have time to read lengthy emails? The Auto-GPT Email Plugin utilizes Auto-GPT's advanced natural language processing capabilities to generate concise and meaningful summaries, keeping you informed without the need to read entire emails.

- **Personalized Newsletters**: Leverage Auto-GPT's creativity and language prowess to create tailored newsletters for your audience. Keep your subscribers engaged with captivating content generated autonomously by AI.

- **Language Translation**: Break the language barrier with Auto-GPT's ability to translate emails to and from multiple languages. Communicate effortlessly with your global contacts, all thanks to the Auto-GPT Email Plugin.

- **Spam Filtering**: Tired of spam cluttering your inbox? Auto-GPT can analyze incoming emails, detect and filter out spam, and ensure you only receive the messages that matter.



## 🚀 Installation

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
EMAIL_MARK_AS_READ=False
```

- Set `EMAIL_ADDRESS` to your sender email address.
- Set `EMAIL_PASSWORD` to your SMTP password. For Gmail, use an [App Password](https://myaccount.google.com/apppasswords).
- If you're not using Gmail, adjust the `EMAIL_SMTP_HOST`, `EMAIL_IMAP_SERVER`, and `EMAIL_SMTP_PORT` values according to your email provider's settings.
- By default, processed emails are not marked as read. If you want to change this behavior, set `EMAIL_MARK_AS_READ` to `True`.

### 10. Allowlist Plugin
In your `.env` search for `ALLOWLISTED_PLUGINS` and add this Plugin:

```ini
################################################################################
### ALLOWLISTED PLUGINS
################################################################################

#ALLOWLISTED_PLUGINS - Sets the listed plugins that are allowed (Example: plugin1,plugin2,plugin3)
ALLOWLISTED_PLUGINS=AutoGPTEmailPlugin
```

## 🤖 Test the Auto-GPT Email Plugin

Experience the plugin's capabilities by testing it for sending and receiving emails.

### A. Test Sending Emails

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

### B. Test Receiving Emails and Replying Back

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
