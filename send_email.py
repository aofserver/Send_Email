# ref: https://towardsdatascience.com/how-to-easily-automate-emails-with-python-8b476045c151

# Step 0 : Create Gmail Account
# Step 1 : Enable 2FA in Gmail Account
# Step 2 : Go to https://myaccount.google.com/u/4/apppasswords and Create password for app choose "(Custum Name) Other" 


# import the required modules
import os
import ssl
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

smtp_host = "smtp.gmail.com"
smtp_port = 465

email_sender = "sender@gmail.com"
email_sender_password = "password"
email_receiver = ["receiver@gmail.com"]

def email_send(receiver, subject, message, sender=email_sender, password=email_sender_password, attachments=[], body_type="html"):
    # defaul sender=username. You can also specify here an alias, like "Name Surname <name.surname@example.com>"
    # email_receiver = list object with recipient(s) email addresses
    # subject = email subject
    # message = email body
    # attachments = list object with attachments path, default no attachments
    # body-type can be "html" (default, if not specified) or "plain"

	msg = MIMEMultipart()
	msg['Subject'] = subject
	msg['From'] = sender

	# add the body
	msg.attach(MIMEText(message, body_type))

	# add attachhments
	if len(attachments)>0:
		for i in attachments:
			filename = i
			attachment = open(i, "rb") # open the file to be sent
			p = MIMEBase('application', 'octet-stream') # instance of MIMEBase and named as p
			p.set_payload((attachment).read()) # To change the payload into encoded form
			encoders.encode_base64(p) # encode into base64
			p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
			msg.attach(p) # attach the instance 'p' to instance 'msg'

	# Converts the Multipart msg into a string
	text = msg.as_string()

	# Send the email(s)
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
		smtp.login(sender, password)
		smtp.sendmail(sender, receiver, text)
		print(f"Sending email {receiver}")


    
text = "TEST1"
email_send(email_receiver, "TEST PLAIN TEXT", text, email_sender, email_sender_password, ["test.txt"], "plain")

html = """
        <html>
            <body>
                <h1 style="color:red; text-align: center;">Test Email Sending</h1>
                <p style="color:blue; text-align: center;">test test test test test test test test test test test test test test test test test test</p>
            </body>
        </html>
       """
email_send(email_receiver, "TEST HTML", html, email_sender, email_sender_password, ["test.txt"], "html")

