import logging

import jwt
from django.http import HttpResponse
from rest_framework import exceptions, status
from rest_framework.decorators import (authentication_classes,
                                       permission_classes)
from rest_framework.response import Response

from Account.models import *
from backend.settings import SIMPLE_JWT

logger = logging.getLogger(__name__)

class TokenMiddleware:
  def __init__(self, get_response) -> None:
    self.get_response = get_response

  def __call__(self, request, *args, **kwds):
    logger.warning("Token middleware")
    logger.warning(request.path)
    if request.path == '/api/login' or request.path == '/' or request.path.startswith('/admin'):
      response = self.get_response(request) 
      return response

    token = request.headers.get('Authorization')
    logger.warning('token')
    logger.warning(token)
    logger.warning('token')
    try:
      token = request.headers.get('Authorization').split()
      logger.warning(token)
      payload = jwt.decode(
        token[1],
        SIMPLE_JWT['SIGNING_KEY'],
        algorithms=[SIMPLE_JWT['ALGORITHM']])
      logger.warning(payload)

      if request.path == '/api/user/create' and payload['role'] != Roles.ADMIN:
        message = {'message': "Unauthorized access"}
        return HttpResponse(str(message), status=status.HTTP_401_UNAUTHORIZED)
      
      if request.path.startswith('/api/password/update') and payload['role'] != Roles.STUDENT:
        message = {'message': "Unauthorized access"}
        return HttpResponse(str(message), status=status.HTTP_401_UNAUTHORIZED)

      if request.path.startswith('/api/user/update') and payload['role'] == Roles.STUDENT:
        message = {'message': "Unauthorized access"}
        return HttpResponse(str(message), status=status.HTTP_401_UNAUTHORIZED)

      logger.warning('valid token')
      response = self.get_response(request) 
      logger.warning(request.path)
      return response
    # token is valid
    except Exception as e:
      message = {'message': "Invalid/ Expired token"}
      return HttpResponse(str(message), status=status.HTTP_401_UNAUTHORIZED)
