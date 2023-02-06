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
    # request.data['password'] = make_password(request.data["password"])
    userSerializer = UserSerializer(data=request.data)
    # logger.warning(request.data)
    # try: 
    #   userSerializer.is_valid(raise_exception=True)
    # except Exception as e:
    #   logger.warning(e)
    #   return Response("exception")
    # logger.warning(userSerializer.is_valid(raise_exception=True))
    if userSerializer.is_valid():
      userSerializer.save()
      message = {"message": "User Created"}
      return Response(message, status=status.HTTP_200_OK)
  except Exception as e:
    logger.warning(e)
    message = {"message": str(e)}
    return Response(message, status=status.HTTP_400_BAD_REQUEST)
  # logger.warning(userSerializer.error)
  message = {"message": "Error: Invalid data"}
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
  student = User.objects.filter(role=Roles.STUDENT)
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
    error = {"message": "Error: User not found"}
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
    error = {"message": "Error: User not found"}
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
    message = {"message": "Successfully updated"}
    return Response(message, status=status.HTTP_200_OK)
  return Response("false", status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([])
@permission_classes([])
def deleteInfo(request, username):
  try:
    user = User.objects.get(userName=username)
    logger.warning(user)
  except Exception as e:
    error = {"message": "Error: User not found"}
    return Response(error, status=status.HTTP_404_NOT_FOUND)
  logger.warning(user)
  user.delete()
  logger.warning('deleted')
  message = {'message': 'Account deleted successfully'}
  return Response(message, status=status.HTTP_200_OK)

@api_view(['POST'])
def login(request):
  data = json.loads(request.body)
  logger.warning(data)
  username = data['userName']
  password = data['password']
  try:
    user = User.objects.get(userName = username, password = password)
    # if check_password(data['password'], user.password):
    access = AccessToken.for_user(user)
    access['role'] = user.role
    access['username'] = user.userName
    roleNames = ["Admin", "Account Staff", "Entry Staff", "Student"] 
    data = {'access': str(access), 'role': user.role, 'roleName': roleNames[user.role - 1], 'username': user.userName, 'user_id': user.pk}
    return Response(data, status=status.HTTP_200_OK)
  except Exception as e:
    message = {"message": "Invalid Username/password"}
    return Response(message,  status=status.HTTP_404_NOT_FOUND)
  message = {"message": "Invalid Username/password"}
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
  # if not check_password(data['currentPassword'], user.password):
  #   return Response("Old Password is incorrect")
  # if check_password(data['newPassword'], user.password):
  #   return Response("Same password")
  # if not data['newPassword'] == data['reEnteredPassword']:
  #   return Response("confirm password not correct")
  # user.password = make_password(data['newPassword'])
  # user.save(update_fields=["password"])
  # return Response("password changed", status=status.HTTP_200_OK)
  
  if not (data['currentPassword'] == user.password):
    message = {'message': "Current Password incorrect"}
    return Response(message, status=status.HTTP_400_BAD_REQUEST)
  if (data['newPassword'] == user.password):
    message = {'message': "New password must differ from current password"}
    return Response(message, status=status.HTTP_400_BAD_REQUEST)
  if not (data['newPassword'] == data['reEnteredPassword']):
    message = {'message': "New password and confirm password mismatched"}
    return Response(message, status=status.HTTP_400_BAD_REQUEST)
  user.password = data['newPassword']
  user.save(update_fields = ['password'])
  message = {'message': "Password changed"}
  return Response(message, status=status.HTTP_200_OK)
  


