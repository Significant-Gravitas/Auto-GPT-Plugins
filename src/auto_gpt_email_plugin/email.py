# email imports
import os
import json
import smtplib
import email
import imaplib
import mimetypes
import time
import autogpt
from email.header import decode_header
from email.message import EmailMessage


email_sender = os.getenv("EMAIL_ADDRESS")
email_password = os.getenv("EMAIL_PASSWORD")
signature = os.getenv("EMAIL_SIGNATURE")
imap_server = os.getenv("EMAIL_IMAP_SERVER")


def send_email(recipient: str, subject: str, message: str) -> str:
    return send_email_with_attachment(recipient, subject, message, None)


def send_email_with_attachment(
    recipient: str, subject: str, message: str, attachment: str
) -> str:
    """Send an email

    Args:
        recipient (str): The email of the recipients
        subject (str): The subject of the email
        message (str): The message content of the email

    Returns:
        str: Any error messages
    """
    if not email_sender:
        return "Error: email not sent. EMAIL_ADDRESS not set in environment."
    elif not email_password:
        return "Error: email not sent. EMAIL_PASSWORD not set in environment."

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = email_sender
    msg["To"] = recipient

    if signature:
        message += f"\n{signature}"

    msg.set_content(message)

    if attachment:
        relative_path = autogpt.workspace.path_in_workspace(attachment)
        ctype, encoding = mimetypes.guess_type(relative_path)
        if ctype is None or encoding is not None:
            # No guess could be made, or the file is encoded (compressed)
            ctype = "application/octet-stream"
        maintype, subtype = ctype.split("/", 1)
        with open(relative_path, "rb") as fp:
            msg.add_attachment(
                fp.read(), maintype=maintype, subtype=subtype, filename=attachment
            )

    draft_folder = os.getenv("EMAIL_DRAFT_MODE_WITH_FOLDER")

    if not draft_folder:
        smtp_host = os.getenv("EMAIL_SMTP_HOST")
        smtp_port = os.getenv("EMAIL_SMTP_PORT")
        # send email
        with smtplib.SMTP(smtp_host, smtp_port) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(email_sender, email_password)
            smtp.send_message(msg)
        return f"Email was sent to {recipient}!"
    else:
        conn = imapOpen(draft_folder)
        conn.select(draft_folder)
        conn.append(
            draft_folder,
            "",
            imaplib.Time2Internaldate(time.time()),
            str(msg).encode("UTF-8"),
        )
        return f"Email went to {draft_folder}!"


def read_emails(imap_folder: str = "inbox", imap_search_command: str = "UNSEEN") -> str:
    """Read emails

    Args:
        recipient (str): The email of the recipients
        subject (str): The subject of the email
        message (str): The message content of the email

    Returns:
        str: Any error messages
    """

    mark_as_read = os.getenv("EMAIL_MARK_AS_SEEN")
    if isinstance(mark_as_read, str):
        mark_as_read = json.loads(mark_as_read.lower())

    conn = imapOpen(imap_folder)
    _, search_data = conn.search(None, imap_search_command)

    messages = []
    for num in search_data[0].split():
        if mark_as_read:
            _, msg_data = conn.fetch(num, "(RFC822)")
        else:
            _, msg_data = conn.fetch(num, "(BODY.PEEK[])")
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

                messages.append(
                    {
                        "From": from_address,
                        "To": to_address,
                        "Date": date,
                        "CC": cc,
                        "Subject": subject,
                        "Message Body": body,
                    }
                )

    conn.logout()
    if not messages:
        return f"There are no Emails in your folder `{imap_folder}` when searching with imap command `{imap_search_command}`"
    return messages


def imapOpen(imap_folder: str) -> imaplib.IMAP4_SSL:
    conn = imaplib.IMAP4_SSL(imap_server)
    conn.login(email_sender, email_password)
    conn.select(imap_folder)
    return conn


def get_email_body(msg: email.message.Message) -> str:
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if content_type == "text/plain" and "attachment" not in content_disposition:
                return part.get_payload(decode=True).decode()
    else:
        return msg.get_payload(decode=True).decode()
