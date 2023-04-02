import logging
import re

from django.core.exceptions import ValidationError
from django.db import models
from rest_framework.response import Response

logger = logging.getLogger(__name__)


def validate_password(value):
    message = None
    logger.warning(value)
    pattern = r'^(?=.*\d)(?=.*[a-zA-Z])(?=.*[^\da-zA-Z\s]).{8,}$'
    if not re.match(pattern, value):
        logger.warning(value)
        message = {'message': 'Invalid password pattern'}
        return message
    return message
