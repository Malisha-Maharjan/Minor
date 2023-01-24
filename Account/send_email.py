import logging
import smtplib

logger = logging.getLogger(__name__)
from django.core.mail import EmailMessage, send_mail

from backend.settings import EMAIL_HOST_USER

# def sendEmail(user, bill):
#   gmail_user = 'studentportal61@gmail.com'
#   gmail_password = 'ufnlsqkiisjsroyj'
#   list = [user.email]

#   sent_from = gmail_user
#   to = list
#   subject = 'Email Notifications'
#   body = 'Check it out!!! hamro milyo'

#   email_text = """\
#   From: %s
#   To: %s
#   Subject: %s

#   %s
#   """ % (sent_from, ", ".join(to), subject, body)


#   server = smtplib.SMTP_SSL('smtp.gmail.com:465')
#   server.ehlo()
#   server.login(gmail_user, gmail_password)

#   server.sendmail(sent_from, to, email_text)
#   server.close()
#   print('Email sent!')

def sendEmail(user):
  logger.warning('sending email')
  subject = 'welcome to GFG world'
  message = f'Hi {user.userName}, thank you for registering in geeksforgeeks.'
  email_from = EMAIL_HOST_USER
  recipient_list = [user.email, ]
  logger.warning('sending messages')
  send_mail( subject, message, email_from, recipient_list )
  # logger.warning(EMAIL_HOST_USER)
  # send_mail(
  #   'welcome to GFG world',
  #   f'Hi {user.userName}, thank you for registering in geeksforgeeks.',
  #   EMAIL_HOST_USER,
  #   [user.email],
  #   fail_silently = False
  # )
  # logger.warning(EMAIL_HOST_USER)
