import json
import logging

# from rest_framework_simplejwt.utils import 
from django.db import connection
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

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
  logger.warning(userSerializer)
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
def getInfo(request, id):
  student = User.objects.get(pk=id)
  serializer = UserSerializer(student)
  return Response(serializer.data)

@api_view(['PUT'])
@authentication_classes([])
@permission_classes([])
def updateInfo(request, id):
  user = User.objects.get(pk=id)
  logger.warning(user)
  serializer = UserSerializer(user, data=request.data, partial=True)
  if serializer.is_valid():
    serializer.save()
    return Response("true", status=status.HTTP_200_OK)
  return Response("false", status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([])
@permission_classes([])
def deleteInfo(request, id):
  user = User.objects.get(pk=id)
  user.delete()
  return Response("true", status=status.HTTP_200_OK)

@api_view(['POST'])
def login(request):
  data = json.loads(request.body)
  username = data['username']
  password = data['password']
  try:
    user = User.objects.get(userName = username, password = password)
    access = AccessToken.for_user(user)
    access['role'] = user.role
    userdata = UserSerializer(user)
    data = {'access': str(access), 'user': userdata.data}
    return Response(data, status=status.HTTP_200_OK)
  except Exception as e:
    return Response('false', status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def student(request, id):
  logger.warning('fee')
  user = User.objects.get(pk=id)
  serializer = StudentSerializer(data=request.data)  
  if serializer.is_valid():
    logger.warning(serializer.data)
    student = Student(
      student=user,
      totalFee = serializer.data['totalFee']
    )
    logger.warning(serializer.data)
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
def details(request, username):
  user = User.objects.get(userName = username)
  student = Student.objects.get(student__userName = username)
  serializer = UserSerializer(user)
  StudentSerializer = StudentDetailsSerializer(user)
  logger.warning(student)
  return Response(StudentSerializer.data)
