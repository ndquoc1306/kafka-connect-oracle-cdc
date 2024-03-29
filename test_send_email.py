from email.message import EmailMessage
import smtplib
import ssl
email_sender = 'ndquoc0602@gmail.com'
email_password = 'izehfgzgantnqyir'

email_receiver = 'metin93357@sentrau.com'

subject = "New blog has been updated!"
body = """Hope you fun with my blog"""

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())