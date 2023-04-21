"""This is the email plugin for Auto-GPT."""
import os
from typing import Any, Dict, List, Optional, Tuple, TypeVar, TypedDict
from auto_gpt_plugin_template import AutoGPTPluginTemplate

# email imports
import json
import smtplib
import email
import imaplib
from email.header import decode_header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import autogpt

PromptGenerator = TypeVar("PromptGenerator")


class Message(TypedDict):
    role: str
    content: str


class AutoGPTEmailPlugin(AutoGPTPluginTemplate):
    """
    This is the Auto-GPT email plugin.
    """

    def __init__(self):
        super().__init__()
        self._name = "Auto-GPT-Email-Plugin"
        self._version = "0.1.0"
        self._description = "Auto-GPT Email Plugin: Supercharge email management."

    def post_prompt(self, prompt: PromptGenerator) -> PromptGenerator:
        prompt.add_command(
            "Read Emails",
            "read_emails",
            {
                "imap_folder": "<imap_folder>",
                "imap_search_command":
                "<imap_search_criteria_command>"
            },
            read_emails)
        prompt.add_command(
            "Send Email",
            "send_email",
            {
                "to": "<to>",
                "subject": "<subject>",
                "body": "<body>"
            },
            send_email
        )
        prompt.add_command(
            "Send Email",
            "send_email_with_attachment",
            {
                "to": "<to>",
                "subject": "<subject>",
                "body": "<body>",
                "attachment": "<path_to_file>"
            },
            send_email_with_attachment
        )

        return prompt

    def can_handle_post_prompt(self) -> bool:
        """This method is called to check that the plugin can
        handle the post_prompt method.

        Returns:
            bool: True if the plugin can handle the post_prompt method."""
        return True

    def can_handle_on_response(self) -> bool:
        """This method is called to check that the plugin can
        handle the on_response method.

        Returns:
            bool: True if the plugin can handle the on_response method."""
        return False

    def on_response(self, response: str, *args, **kwargs) -> str:
        """This method is called when a response is received from the model."""
        pass

    def can_handle_on_planning(self) -> bool:
        """This method is called to check that the plugin can
        handle the on_planning method.

        Returns:
            bool: True if the plugin can handle the on_planning method."""
        return False

    def on_planning(
        self, prompt: PromptGenerator, messages: List[Message]
    ) -> Optional[str]:
        """This method is called before the planning chat completion is done.

        Args:
            prompt (PromptGenerator): The prompt generator.
            messages (List[str]): The list of messages.
        """
        pass

    def can_handle_post_planning(self) -> bool:
        """This method is called to check that the plugin can
        handle the post_planning method.

        Returns:
            bool: True if the plugin can handle the post_planning method."""
        return False

    def post_planning(self, response: str) -> str:
        """This method is called after the planning chat completion is done.

        Args:
            response (str): The response.

        Returns:
            str: The resulting response.
        """
        pass

    def can_handle_pre_instruction(self) -> bool:
        """This method is called to check that the plugin can
        handle the pre_instruction method.

        Returns:
            bool: True if the plugin can handle the pre_instruction method."""
        return False

    def pre_instruction(self, messages: List[Message]) -> List[Message]:
        """This method is called before the instruction chat is done.

        Args:
            messages (List[Message]): The list of context messages.

        Returns:
            List[Message]: The resulting list of messages.
        """
        pass

    def can_handle_on_instruction(self) -> bool:
        """This method is called to check that the plugin can
        handle the on_instruction method.

        Returns:
            bool: True if the plugin can handle the on_instruction method."""
        return False

    def on_instruction(self, messages: List[Message]) -> Optional[str]:
        """This method is called when the instruction chat is done.

        Args:
            messages (List[Message]): The list of context messages.

        Returns:
            Optional[str]: The resulting message.
        """
        pass

    def can_handle_post_instruction(self) -> bool:
        """This method is called to check that the plugin can
        handle the post_instruction method.

        Returns:
            bool: True if the plugin can handle the post_instruction method."""
        return False

    def post_instruction(self, response: str) -> str:
        """This method is called after the instruction chat is done.

        Args:
            response (str): The response.

        Returns:
            str: The resulting response.
        """
        pass

    def can_handle_pre_command(self) -> bool:
        """This method is called to check that the plugin can
        handle the pre_command method.

        Returns:
            bool: True if the plugin can handle the pre_command method."""
        return False

    def pre_command(
        self, command_name: str, arguments: Dict[str, Any]
    ) -> Tuple[str, Dict[str, Any]]:
        """This method is called before the command is executed.

        Args:
            command_name (str): The command name.
            arguments (Dict[str, Any]): The arguments.

        Returns:
            Tuple[str, Dict[str, Any]]: The command name and the arguments.
        """
        pass

    def can_handle_post_command(self) -> bool:
        """This method is called to check that the plugin can
        handle the post_command method.

        Returns:
            bool: True if the plugin can handle the post_command method."""
        return False

    def post_command(self, command_name: str, response: str) -> str:
        """This method is called after the command is executed.

        Args:
            command_name (str): The command name.
            response (str): The response.

        Returns:
            str: The resulting response.
        """
        pass

    def can_handle_chat_completion(
        self, messages: Dict[Any, Any], model: str, temperature: float, max_tokens: int
    ) -> bool:
        """This method is called to check that the plugin can
          handle the chat_completion method.

        Args:
            messages (List[Message]): The messages.
            model (str): The model name.
            temperature (float): The temperature.
            max_tokens (int): The max tokens.

          Returns:
              bool: True if the plugin can handle the chat_completion method."""
        return False

    def handle_chat_completion(
        self, messages: List[Message], model: str, temperature: float, max_tokens: int
    ) -> str:
        """This method is called when the chat completion is done.

        Args:
            messages (List[Message]): The messages.
            model (str): The model name.
            temperature (float): The temperature.
            max_tokens (int): The max tokens.

        Returns:
            str: The resulting response.
        """
        pass


email_sender = os.getenv("EMAIL_ADDRESS")
email_password = os.getenv("EMAIL_PASSWORD")
signature = os.getenv("EMAIL_SIGNATURE")

def send_email(recipient: str, subject: str, message: str) -> str:
    return send_email_with_attachment(recipient, subject, message, None)

def send_email_with_attachment(recipient: str, subject: str, message: str, attachment: str) -> str:
    """Send an email

    Args:
        recipient (str): The email of the recipients
        subject (str): The subject of the email
        message (str): The message content of the email

    Returns:
        str: Any error messages
    """
    smtp_host = os.getenv("EMAIL_SMTP_HOST")
    smtp_port = os.getenv("EMAIL_SMTP_PORT")

    if not email_sender:
        return "Error: email not sent. EMAIL_ADDRESS not set in environment."
    elif not email_password:
        return "Error: email not sent. EMAIL_PASSWORD not set in environment."

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = email_sender
    msg['To'] = recipient

    if signature:
        message += f"\n{signature}"

    msg.attach(MIMEText(message))

    if attachment:
        relative_path = autogpt.workspace.path_in_workspace(attachment)
        mime_attachment = MIMEApplication(open(relative_path, 'rb').read())
        mime_attachment.add_header('Content-Disposition', 'attachment', filename= attachment)
        msg.attach(mime_attachment)

    # send email
    with smtplib.SMTP(smtp_host, smtp_port) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(email_sender, email_password)
        smtp.send_message(msg)
    return "Email was sent!"



def read_emails(imap_folder: str = "inbox", imap_search_command: str = "UNSEEN") -> str:
    """Read emails

    Args:
        recipient (str): The email of the recipients
        subject (str): The subject of the email
        message (str): The message content of the email

    Returns:
        str: Any error messages
    """
    imap_server = os.getenv("EMAIL_IMAP_SERVER")
    mark_as_read = os.getenv("EMAIL_MARK_AS_SEEN")
    if isinstance(mark_as_read, str):
        mark_as_read = json.loads(mark_as_read.lower())
    
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(email_sender, email_password)
    mail.select(imap_folder)
    _, search_data = mail.search(None, imap_search_command)

    messages = []
    for num in search_data[0].split():
        if mark_as_read:
            _, msg_data = mail.fetch(num, "(RFC822)")
        else:
            _, msg_data = mail.fetch(num, "(BODY.PEEK[])")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])

                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding)

                body = get_email_body(msg)
                from_address = msg["From"]
                to_address = msg["To"]
                date = msg["Date"]
                cc = msg["CC"] if msg["CC"] else ""

                messages.append({
                    "From": from_address,
                    "To": to_address,
                    "Date": date,
                    "CC": cc,
                    "Subject": subject,
                    "Message Body": body
                })

    mail.logout()
    if not messages:
        return f"There are no Emails in your folder `{imap_folder}` when searching with imap command `{imap_search_command}`"
    return messages


def get_email_body(msg: email.message.Message) -> str:
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if content_type == "text/plain" and "attachment" not in content_disposition:
                return part.get_payload(decode=True).decode()
    else:
        return msg.get_payload(decode=True).decode()
