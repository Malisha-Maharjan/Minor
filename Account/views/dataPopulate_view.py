import logging

from ..models import *

logger = logging.getLogger(__name__)

from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)

# @api_view(['GET'])
# @authentication_classes([])
# @permission_classes([])
# def userAdd():
#   for i in range(2):
#     user=User(
#       userName = f"username{i}",
#       firstName = f"student{i}",
#       lastName = f"student{i}",

#     )
