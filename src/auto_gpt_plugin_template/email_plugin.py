import os
import smtplib
import email
import imaplib
from email.message import EmailMessage
from email.header import decode_header

email_sender = os.getenv("EMAIL_ADDRESS")
email_password = os.getenv("EMAIL_PASSWORD")


def send_email(recipient: str, subject: str, message: str) -> str:
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

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = email_sender
    msg['To'] = recipient
    msg.set_content(message)

    # send email
    with smtplib.SMTP(smtp_host, smtp_port) as smtp:
        smtp.starttls()
        smtp.login(email_sender, email_password)
        smtp.send_message(msg)


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
    mark_as_read = os.getenv("EMAIL_MARK_AS_READ")

    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(email_sender, email_password)
    mail.select(imap_folder)
    _, search_data = mail.search(None, imap_search_command)

    messages = []
    for num in search_data[0].split():
        if mark_as_read:
            _, msg_data = mail.fetch(num, "(BODY.PEEK[])")
        else:
            _, msg_data = mail.fetch(num, "(RFC822)")
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
