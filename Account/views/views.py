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
cursor=connection.cursor()

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def userCreate(request):
  message=""
  userSerializer = UserSerializer(data=request.data)
  if userSerializer.is_valid():
    user = User(
      userName=userSerializer.data['userName'],
      firstName=userSerializer.data['firstName'],
      lastName=userSerializer.data['lastName'],
      password=userSerializer.data['password'],
      role=userSerializer.data['role']
    ) 
    user.save()
    message = "true"
    return Response(message, status=status.HTTP_200_OK)
  message = "false"
  return Response(message, status=status.HTTP_400_BAD_REQUEST)

# select * from users where username='' and password = ''

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def getAllInfo(request):
  student = User.objects.all()
  serializer = UserSerializer(student, many=True)
  return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def getInfo(request, username):
  student = User.objects.get(userName=username)
  serializer = UserSerializer(student)
  return Response(serializer.data)

@api_view(['PUT'])
@authentication_classes([])
@permission_classes([])
def updateInfo(request, username):
  user = User.objects.get(userName=username)
  logger.warning(user)
  serializer = UserSerializer(user, data=request.data, partial=True)
  if serializer.is_valid():
    serializer.save()
    return Response("true", status=status.HTTP_200_OK)
  return Response("false", status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([])
@permission_classes([])
def deleteInfo(request, username):
  user = User.objects.get(userName=username)
  user.delete()
  return Response("true", status=status.HTTP_200_OK)

@api_view(['POST'])
def login(request):
  data = json.loads(request.body)
  username = data['userName']
  password = data['password']
  try:
    user = User.objects.get(userName = username, password = password)
    access = AccessToken.for_user(user)
    access['role'] = user.role
    access['username'] = user.userName
    data = {'access': str(access)}
    return Response(data, status=status.HTTP_200_OK)
  except Exception as e:
    return Response('false', status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def studentRegistration(request, username):
  logger.warning('fee')
  user = User.objects.get(userName=username)
  serializer = StudentSerializer(data=request.data)  
  if serializer.is_valid():
    logger.warning(serializer.data)
    student = Student(
      student=user,
      faculty = serializer.data['faculty'],
      batch = serializer.data['batch'],
      semester = serializer.data['semester'],
      totalFee = serializer.data['totalFee'],
    )
    student.save()
    return Response('true', status=status.HTTP_200_OK)
  return Response('false', status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def hello(request):
  logger.warning('hhhh')
  message = {'message': 'hello'}
  
  return Response(message)

@api_view(['GET'])
def studentDetails(request, username):
  logger.warning('details api')
  user = User.objects.get(userName = username)
  # student = Student.objects.get(student__userName=username)
  StudentSerializer = StudentDetailsSerializer(user)
  logger.warning(StudentSerializer.data)
  return Response(StudentSerializer.data)




