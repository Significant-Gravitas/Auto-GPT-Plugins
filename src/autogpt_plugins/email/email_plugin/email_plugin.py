import email
import imaplib
import json
import mimetypes
import os
import re
import smtplib
import time
from email.header import decode_header
from email.message import EmailMessage
from bs4 import BeautifulSoup



def bothEmailAndPwdSet() -> bool:
    return True if os.getenv("EMAIL_ADDRESS") and os.getenv("EMAIL_PASSWORD") else False


def getSender():
    email_sender = os.getenv("EMAIL_ADDRESS")
    if not email_sender:
        return "Error: email not sent. EMAIL_ADDRESS not set in environment."
    return email_sender


def getPwd():
    email_password = os.getenv("EMAIL_PASSWORD")
    if not email_password:
        return "Error: email not sent. EMAIL_PASSWORD not set in environment."
    return email_password


def send_email(to: str, subject: str, body: str) -> str:
    return send_email_with_attachment_internal(to, subject, body, None, None)


def send_email_with_attachment(to: str, subject: str, body: str, filename: str) -> str:
    attachment_path = filename
    attachment = os.path.basename(filename)
    return send_email_with_attachment_internal(
        to, subject, body, attachment_path, attachment
    )


def send_email_with_attachment_internal(
    to: str, title: str, message: str, attachment_path: str, attachment: str
) -> str:
    """Send an email

    Args:
        to (str): The email of the recipient
        title (str): The title of the email
        message (str): The message content of the email

    Returns:
        str: Any error messages
    """
    email_sender = getSender()
    email_password = getPwd()

    msg = EmailMessage()
    msg["Subject"] = title
    msg["From"] = email_sender
    msg["To"] = to

    signature = os.getenv("EMAIL_SIGNATURE")
    if signature:
        message += f"\n{signature}"

    msg.set_content(message)

    if attachment_path:
        ctype, encoding = mimetypes.guess_type(attachment_path)
        if ctype is None or encoding is not None:
            # No guess could be made, or the file is encoded (compressed)
            ctype = "application/octet-stream"
        maintype, subtype = ctype.split("/", 1)
        with open(attachment_path, "rb") as fp:
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
            smtp.quit()
        return f"Email was sent to {to}!"
    else:
        conn = imap_open(draft_folder, email_sender, email_password)
        conn.append(
            draft_folder,
            "",
            imaplib.Time2Internaldate(time.time()),
            str(msg).encode("UTF-8"),
        )
        return f"Email went to {draft_folder}!"


def read_emails(
        imap_folder: str = "inbox", imap_search_command: str = "UNSEEN", limit: int = 5,
        page: int = 1) -> str:
    """Read emails from an IMAP mailbox.

    This function reads emails from a specified IMAP folder, using a given IMAP search command, limits, and page numbers.
    It returns a list of emails with their details, including the sender, recipient, date, CC, subject, and message body.

    Args:
        imap_folder (str, optional): The name of the IMAP folder to read emails from. Defaults to "inbox".
        imap_search_command (str, optional): The IMAP search command to filter emails. Defaults to "UNSEEN".
        limit (int, optional): Number of email's the function should return. Defaults to 5 emails.
        page (int, optional): The index of the page result the function should resturn. Defaults to 0, the first page.

    Returns:
        str: A list of dictionaries containing email details if there are any matching emails. Otherwise, returns
             a string indicating that no matching emails were found.
    """
    email_sender = getSender()
    imap_folder = adjust_imap_folder_for_gmail(imap_folder, email_sender)
    imap_folder = enclose_with_quotes(imap_folder)
    imap_search_ar = split_imap_search_command(imap_search_command)
    email_password = getPwd()

    mark_as_seen = os.getenv("EMAIL_MARK_AS_SEEN")
    if isinstance(mark_as_seen, str):
        mark_as_seen = json.loads(mark_as_seen.lower())

    conn = imap_open(imap_folder, email_sender, email_password)

    imap_keyword = imap_search_ar[0]
    if len(imap_search_ar) == 1:
        _, search_data = conn.search(None, imap_keyword)
    else:
        argument = enclose_with_quotes(imap_search_ar[1])
        _, search_data = conn.search(None, imap_keyword, argument)

    messages = []
    for num in search_data[0].split():
        if mark_as_seen:
            message_parts = "(RFC822)"
        else:
            message_parts = "(BODY.PEEK[])"
        _, msg_data = conn.fetch(num, message_parts)
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                
                # If the subject has unknown encoding, return blank
                if msg["Subject"] is not None:
                    subject, encoding = decode_header(msg["Subject"])[0]
                else:
                    subject = ""
                    encoding = ""


                if isinstance(subject, bytes):
                    try:
                        # If the subject has unknown encoding, return blank
                        if encoding is not None:
                            subject = subject.decode(encoding)
                        else:
                            subject = ""
                    except [LookupError] as e:
                        pass

                body = get_email_body(msg)
                # Clean email body
                body = clean_email_body(body)

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
        return (
            f"There are no Emails in your folder `{imap_folder}` "
            f"when searching with imap command `{imap_search_command}`"
        )

    # Confirm that integer parameters are the right type
    limit = int(limit)
    page = int(page)

    # Validate parameter values
    if limit < 1:
        raise ValueError("Error: The message limit should be 1 or greater")

    page_count = len(messages) // limit + (len(messages) % limit > 0)

    if page < 1 or page > page_count:
        raise ValueError("Error: The page value references a page that is not part of the results")

    # Calculate paginated indexes
    start_index = len(messages) - (page * limit + 1)
    end_index = start_index + limit
    start_index = max(start_index, 0)

    # Return paginated indexes
    if start_index == end_index:
        return [messages[start_index]]
    else:
        return messages[start_index:end_index]


def adjust_imap_folder_for_gmail(imap_folder: str, email_sender: str) -> str:
    if "@gmail" in email_sender.lower() or "@googlemail" in email_sender.lower():
        if "sent" in imap_folder.lower():
            return '"[Gmail]/Sent Mail"'
        if "draft" in imap_folder.lower():
            return "[Gmail]/Drafts"
    return imap_folder


def imap_open(
    imap_folder: str, email_sender: str, email_password: str
) -> imaplib.IMAP4_SSL:
    imap_server = os.getenv("EMAIL_IMAP_SERVER")
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
                # If the email body has unknown encoding, return null
                try:
                    return part.get_payload(decode=True).decode()
                except UnicodeDecodeError as e:
                    pass
    else:
        try:
            # If the email body has unknown encoding, return null
            return msg.get_payload(decode=True).decode()
        except UnicodeDecodeError as e:
            pass

def enclose_with_quotes(s):
    # Check if string contains whitespace
    has_whitespace = bool(re.search(r"\s", s))

    # Check if string is already enclosed by quotes
    is_enclosed = s.startswith(("'", '"')) and s.endswith(("'", '"'))

    # If string has whitespace and is not enclosed by quotes, enclose it with double quotes
    if has_whitespace and not is_enclosed:
        return f'"{s}"'
    else:
        return s


def split_imap_search_command(input_string):
    input_string = input_string.strip()
    parts = input_string.split(maxsplit=1)
    parts = [part.strip() for part in parts]

    return parts

def clean_email_body(email_body):
    """Remove formating and URL's from an email's body

    Args:
        email_body (str, optional): The email's body

    Returns:
        str: The email's body without any formating or URL's
    """

    # If body is None, return an empty string
    if email_body is None: email_body = ""

    # Remove any HTML tags
    email_body = BeautifulSoup(email_body, "html.parser")
    email_body = email_body.get_text()

    # Remove return characters
    email_body = "".join(email_body.splitlines())

    # Remove extra spaces
    email_body = " ".join(email_body.split())

    # Remove unicode characters
    email_body = email_body.encode("ascii", "ignore")
    email_body = email_body.decode("utf-8", "ignore")

    # Remove any remaining URL's
    email_body = re.sub(r"http\S+", "", email_body)

    return email_body
