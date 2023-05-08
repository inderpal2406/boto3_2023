"""Module to send an email with & without attachment using Amazon SES via AWS SDK boto3"""

# Multipurpose Internet Mail Extensions (MIME) is an Internet standard that
# extends the format of email messages to support text in character sets other
# than ASCII, as well as attachments of audio, video, images, and application
# programs. Message bodies may consist of multiple parts, and header information
# may be specified in non-ASCII character sets. Email messages with MIME formatting
# are typically transmitted with standard protocols, such as the Simple Mail Transfer
# Protocol (SMTP), the Post Office Protocol (POP), and the Internet Message Access 
# Protocol (IMAP).

# Import modules.

import boto3
from datetime import datetime
from email.mime.multipart import MIMEMultipart  # class MIMEMultipart in module email.mime.multipart
# Above class for MIME multipart/* type messages.
from email.mime.text import MIMEText  # class MIMEText in module email.mime.text
# Above class for generating text/* type MIME documents.
from email.mime.application import MIMEApplication  # class MIMEApplication in module email.mime.application
# above class for generating application/* MIME documents.

# Define functions.

def main():
    """First function to be called"""
    sender = "inderpal2406@gmail.com"
    to = "inderpal7738@gmail.com"
    timestamp = datetime.now().strftime("%a %d-%b-%Y")
    aws_region = "ap-south-1"
    subject = "Test email with attachment using Amazon SES"
    body_text = "Hello,\nThis is test email."
    body_html = """
    <html>
    <head></head>
    <body>
    <h1>Hello</h1>
    <p>This is test email.</p>
    </body>
    </html>
    """
    charset = "utf-8"
    aws_session = boto3.session.Session(profile_name="aws-admin")
    ses_client = aws_session.client(service_name="ses",region_name="ap-south-1")
    response = ses_client.send_email(
        Source="inderpal2406@gmail.com",
        Destination={
            "ToAddresses": ["inderpal7738@gmail.com"]
        },
        Message={
            "Subject":{
                "Data": "Test email from Amazon SES.",
                "Charset": "utf-8"
            },
            "Body": {
                "Text": {
                    "Data": "Hello,\n\nThis is test email.\n\nThank You,\nAmazon SES.\n",
                    "Charset": "utf-8"
                }
            }
        }
    )
    print("Email sent without attachment.")
    # Create a multipart parent container of mixed subtype.
    msg = MIMEMultipart(_subtype="mixed")
    # Add from, to & subject lines to parent container.
    msg["From"] = "inderpal2406@gmail.com"
    msg["To"] = "inderpal7738@gmail.com"
    msg["Subject"] = "Test email with attachment."
    # Create a multipart child container of alternative subtype.
    msg_body = MIMEMultipart(_subtype="alternative")
    # Encode the text and HTML content and set the character encoding. This step is
    # necessary if you're sending a message with characters outside the ASCII range.
    textpart = MIMEText(_text=body_text.encode(charset), _subtype="plain", _charset=charset)
    htmlpart = MIMEText(_text=body_html.encode(charset), _subtype="html", _charset=charset)
    # Add text & html parts to the child container.
    msg_body.attach(textpart)
    msg_body.attach(htmlpart)
    # Above method attach is inherited by msg_body object, when msg_body is created from class MIMEMultipart.
    # Define the attachment part and encode it using MIMEApplication.
    att = MIMEApplication(open(".\\attachment.txt","rb").read())
    # Add a header to tell the email client to treat this part as an attachment,
    # and to give the attachment a name.
    att.add_header("Content-Disposition","attachment",filename="attachment.txt")
    # Attach the multipart/alternative child container to the multipart/mixed
    # parent container.
    msg.attach(msg_body)
    # Add the attachment to the parent container.
    msg.attach(att)
    response = ses_client.send_raw_email(
        Source="inderpal2406@gmail.com",
        Destinations=["inderpal7738@gmail.com"],
        RawMessage={
            #'Data': 'From: sender@example.com\nTo: recipient@example.com\nSubject: Test email (contains an attachment)\nMIME-Version: 1.0\nContent-type: Multipart/Mixed; boundary="NextPart"\n\n--NextPart\nContent-Type: text/plain\n\nThis is the message body.\n\n--NextPart\nContent-Type: text/plain;\nContent-Disposition: attachment; filename="attachment.txt"\n\nThis is the text in the attachment.\n\n--NextPart--',
            "Data": msg.as_string()
        }
    )
    print("Email sent with attachment.")

if __name__ == "__main__":
    main()
