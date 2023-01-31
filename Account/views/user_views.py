import json
import logging

# from rest_framework_simplejwt.utils import 
import jwt
from django.contrib.auth.hashers import check_password, make_password
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
  try:
    message=""
    data = json.loads(request.body)
    data['password'] = make_password(data['password'])
    userSerializer = UserSerializer(data=data)
    logger.warning(request.data)
    if userSerializer.is_valid():
      userSerializer.save()
      message = {"message": "true"}
      return Response(message, status=status.HTTP_200_OK)
  except Exception as e:
    logger.warning(e)
    return Response("exception")
  message = {"message": "false"}
  return Response(message, status=status.HTTP_400_BAD_REQUEST)

  # data = json.loads(request.body)
  # try:
  #   user = User(
  #   firstName = data['firstName'],
  #   userName = data['userName'],
  #   lastName = data['lastName'],
  #   password = make_password(data['password']),
  #   role = data['role'],
  #   address = data['address'],
  #   contact_no = data['contact_no'],
  #   email = data['email'],
  #   batch = data['batch'],
  #   faculty = Faculty.objects.get(pk=data['faculty']),
  #   semester = Semester.objects.get(pk=data['semester']))
  #   user.save()
  #   return Response("ok", status=status.HTTP_200_OK)
  # except Exception as e:
  #   logger.warning(e)
  #   return Response("exception", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def getAllInfo(request):
  logger.warning('getting info')
  student = User.objects.all()
  logger.warning('getting info')
  serializer = UserSerializer(student, many=True)
  logger.warning('getting info')
  return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def getInfo(request, username):
  try:
    student = User.objects.get(userName=username)
  except Exception as e:
    error = {"error": str(e)}
    return Response(error, status=status.HTTP_404_NOT_FOUND)
  serializer = UserSerializer(student)
  return Response(serializer.data)

@api_view(['PUT'])
@authentication_classes([])
@permission_classes([])
def updateInfo(request, username):
  try:
    user = User.objects.get(userName=username)
  except Exception as e:
    error = {"error": str(e)}
    return Response(error, status=status.HTTP_404_NOT_FOUND)
  logger.warning(user)
  # data = json.loads(request.body)
  # logger.warning(data['password'])
  # encrypted_password=make_password(data['password'])
  # if not check_password(user.password, encrypted_password):
  #   data['password'] = make_password(data['password'])
  serializer = UserSerializer(user, data=request.data, partial=True)
  if serializer.is_valid():
    serializer.save()
    user = User.objects.get(userName = username)
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)
  return Response("false", status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([])
@permission_classes([])
def deleteInfo(request, username):
  logger.warning('hihihih')
  try:
    user = User.objects.get(userName=username)
    logger.warning(user)
  except Exception as e:
    error = {"error": str(e)}
    return Response(error, status=status.HTTP_404_NOT_FOUND)
  logger.warning(user)
  user.delete()
  logger.warning('deleted')
  return Response("true", status=status.HTTP_200_OK)

@api_view(['POST'])
def login(request):
  data = json.loads(request.body)
  logger.warning(data)
  username = data['userName']
  try:
    user = User.objects.get(userName = username)
    if check_password(data['password'], user.password):
        access = AccessToken.for_user(user)
        access['role'] = user.role
        access['username'] = user.userName
        roleNames = ["Admin", "Account Staff", "Entry Staff", "Student"] 
        data = {'access': str(access), 'role': user.role, 'roleName': roleNames[user.role - 1], 'username': user.userName, 'user_id': user.pk}
        return Response(data, status=status.HTTP_200_OK)
  except Exception as e:
    message = {"error": "Invalid Username/password"}
    return Response(message,  status=status.HTTP_404_NOT_FOUND)
  message = {"error": "Invalid Username/password"}
  return Response(message, status=status.HTTP_401_UNAUTHORIZED)

# @api_view(['GET'])
# @authentication_classes([])
# @permission_classes([])
# def hello(request):
#   logger.warning('hhhh')
#   message = {'message': 'hello'}
  
#   return Response(message)

# @api_view(['GET'])
# def studentDetails(request, username):
#   logger.warning('details api')
#   user = User.objects.get(userName = username)
#   # student = Student.objects.get(student__userName=username)
#   StudentSerializer = StudentDetailsSerializer(user)
#   logger.warning(StudentSerializer.data)
#   return Response(StudentSerializer.data)


# import base64

# from django.core.files.storage import default_storage


# @api_view(['GET'])
# def imageSend(request):
#   images = imageModel.objects.get(pk=1)
#   image_url = str(images.image)
#   # logger.warning(f'{image_url}')
#   # with open("images/Screen_Shot_2020-09-26_at_10.07.13_am.png", "rb") as image_file:
#   encoded_string = base64.b64encode(default_storage.open(image_url, "rb").read()).decode()
#   # serializer = ImageSerializer(images)
#   message = {'image': encoded_string}
#   return Response(message)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def updatePassword(request, username):
  data = json.loads(request.body)
  logger.warning(request.data)
  user = User.objects.get(userName=username)
  logger.warning(user)
  if not check_password(data['password'], user.password):
    return Response("Old Password is incorrect")
  if check_password(data['new_password'], user.password):
    return Response("Same password")
  if not data['new_password'] == data['confirm_password']:
    return Response("confirm password not correct")
  user.password = make_password(data['new_password'])
  user.save(update_fields=["password"])
  return Response("password changed", status=status.HTTP_200_OK)