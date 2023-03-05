import json
import logging

# from rest_framework_simplejwt.utils import 
import jwt
from django.db import connection
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenVerifyView

from backend.settings import SIMPLE_JWT

from ..models import *
from ..serializer import *

logger = logging.getLogger(__name__)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def addSubject(request):
  serializer = SubjectSerializer(data=request.data)
  if not serializer.is_valid():
    error = {"error": serializer.error_messages}
    return Response(error)
  serializer.save()
  return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def getSubject(request, faculty, semester):
  subjects = Subject.objects.filter(faculty__pk=faculty, semester__pk=semester)
  serializer = SubjectSerializer(subjects, many=True)
  return Response(serializer.data, status=status.HTTP_200_OK)



# @api_view(['GET'])
# @authentication_classes([])
# @permission_classes([])
# def getSubject(request, username):
#   student = User.objects.get(userName = username)
#   subjects = Subject.objects.filter(semester__pk=student.semester.pk)
#   serializer = SubjectSerializer(subjects, many=True)
  
#   return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@authentication_classes([])
@permission_classes([])
def deleteSubject(request, faculty, semester, subject):
  subject = Subject.objects.filter(faculty__pk=faculty, semester__pk=semester, subject=subject)
  subject.delete()
  message = {"message": "Successfully deleted"}
  return Response(message, status=status.HTTP_200_OK)