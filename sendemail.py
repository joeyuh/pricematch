import smtplib
import ssl
from email.message import EmailMessage
import imghdr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_an_email(subject, recipient, text_content, html_content):
    email_address = 'gooddealscript@gmail.com'
    email_password = 'whataPassword'

    # formatting the email, creating message, subject, adding a recipient, and adding some text
    msg = MIMEMultipart("alternative")
    msg['Subject'] = subject
    msg['From'] = email_address
    msg['To'] = recipient

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text_content, "plain")
    part2 = MIMEText(html_content, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    msg.attach(part1)
    msg.attach(part2)

    # Legacy
    # try:
    #     for image in image_list:
    #         with open(f'{image}', 'rb') as f:
    #             file_data = f.read()
    #             file_type = imghdr.what(f.name)
    #             file_name = f.name
    #
    #         msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)
    # except:
    #     print('No images found to attach.')

    # context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.sendmail(email_address, recipient, msg.as_string())
