def send_an_email(subject, receiver, message_content):
    import smtplib
    from email.message import EmailMessage
    import imghdr

    email_address = 'gooddealscript@gmail.com'
    email_password = 'whataPassword'

    #formatting the email, creating message, subject, adding a recipient, and adding some text
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = email_address
    msg['To'] = receiver
    msg.set_content(message_content)

    with open('test_image.jpg', 'rb') as f:
        file_data = f.read()
        file_type = imghdr.what(f.name)
        file_name = f.name
    
    msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)

send_an_email(subject='test', receiver='5214894a@gmail.com', message_content='TESTS')



