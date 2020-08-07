def send_an_email(subject, recipient, message_content, image_list=None):
    import smtplib
    from email.message import EmailMessage
    import imghdr

    email_address = 'gooddealscript@gmail.com'
    email_password = 'whataPassword'

    #formatting the email, creating message, subject, adding a recipient, and adding some text
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = email_address
    msg['To'] = recipient
    msg.set_content(message_content)

    try:
        for image in image_list:
            with open(f'{image}', 'rb') as f:
                file_data = f.read()
                file_type = imghdr.what(f.name)
                file_name = f.name
            
            msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)
    except:
        print('No images found to attach.')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)



