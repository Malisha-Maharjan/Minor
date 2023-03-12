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


