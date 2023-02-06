import logging
import smtplib

logger = logging.getLogger(__name__)
from django.core.mail import send_mail

from backend.settings import EMAIL_HOST_USER


def sendEmail(email, subject, body):
  logger.warning('sending email')
  logger.warning(email)
  subject = subject
  message = body
  email_from = EMAIL_HOST_USER
  recipient_list = email
  logger.warning('sending messages')
  send_mail( subject, message, email_from, recipient_list )