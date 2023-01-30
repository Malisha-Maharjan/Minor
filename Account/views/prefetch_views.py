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


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def getFaculty(request):
  faculty = Faculty.objects.all()
  serializer = FacultySerializer(faculty, many=True)
  return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def getSemesters(request):
  semester = Semester.objects.all()
  serializer = SemesterSerializer(semester, many=True)
  return Response(serializer.data)



@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def mark(request):
  marks = json.loads(request.body)
  logger.warning('marks')
  for mark in marks:
    logger.warning(mark)
  return Response('ok')
  # try: 
  #   student = User.objects.get(userName=username)
  #   semester = Semester.objects.get(pk=marks['semester'])
  #   subject = Subject.objects.get(pk=marks['subject'], semester__pk=marks['semester'])
  #   result = Marks(
  #     student = student,
  #     semester = semester,
  #     subject = subject,
  #     marks = marks['marks']
  #   )
  #   logger.warning(result)
  #   result.save()
  #   return Response("ok")
  # except Exception as e:
  #   logger.warning(e)
  #   error = {"error": str(e)}
  #   return Response(error, status=status.HTTP_400_BAD_REQUEST)

