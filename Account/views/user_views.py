import json
import logging

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
from ..send_email import *
from ..serializer import *

logger = logging.getLogger(__name__)
cursor=connection.cursor()

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def userCreate(request):
  try:
    message=""
    # data = json.loads(request.body)
    # request.data['password'] = make_password(request.data["password"])
    userSerializer = UserSerializer(data=request.data)
    logger.warning(request.data)
    try: 
      userSerializer.is_valid(raise_exception=True)
    except Exception as e:
      
      message = {'message': str(e)}
      return Response(message, status=status.HTTP_400_BAD_REQUEST)
    logger.warning(userSerializer.is_valid(raise_exception=True))
    if userSerializer.is_valid():
      # logger.warning(userSerializer)
      userSerializer.save()
      message = {"message": "User Created"}
      email = [userSerializer.data['email']]
      subject = 'Account Created'
      name = userSerializer.data['firstName']
      username = userSerializer.data['userName']
      password = userSerializer.data['password']
      body = f'Dear {name},\n\n Your account has been created for Student Easy Pay and Result Analysis. Following details are your login credentials.\n\n Username = {username}\n Password = {password}\n Note: Please change your password after logged in \n\n Best Regards,\n\n Student Portal'
      sendEmail(email, subject, body)
      return Response(message, status=status.HTTP_200_OK)
  except Exception as e:
    logger.warning(e)
    message = {"message": str(e)}
    logger.warning(e)
    return Response(message, status=status.HTTP_400_BAD_REQUEST)
  # logger.warning(userSerializer.error)
  message = {"message": "Error: Invalid data"}
  return Response(message, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def getAllInfo(request):
  logger.warning('getting info')
  student = User.objects.exclude(role=Roles.ADMIN)
  logger.warning('getting info')
  serializer = UserSerializer(student, many=True)
  logger.warning('getting info')
  return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def getStudent(request):
  data = json.loads(request.body)

  student = User.objects.filter(role=Roles.STUDENT, batch=data['batch'], faculty=data['faculty'])
  serializer = UserSerializer(student, many=True)
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

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def updatePassword(request, username):
  try:
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
    if len(data['currentPassword']) == 0 or len(data['newPassword']) == 0 or len(data['newPassword']) == 0:
      message = {'message': 'Invalid Data'}
      return Response(message, status=status.HTTP_400_BAD_REQUEST)
    message = validate_password(data['newPassword'])
    if message != None:
      return Response(message, status=status.HTTP_400_BAD_REQUEST)
    message = validate_password(data['reEnteredPassword'])
    if message != None:
      return Response(message, status=status.HTTP_400_BAD_REQUEST)
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
  except Exception as e:
    return Response(str(e))
  
  
@api_view(['POST'])
def forgotPassword(request):
  data = json.loads(request.body)
  logger.warning(data)
  if data['username'] == None or data['email'] == None:
    message = {'message': 'Please fill the field'}
    return Response(message, status=status.HTTP_400_BAD_REQUEST)
  if len(data['username']) == 0 or len(data['email']) == 0:
    message = {'message': 'Please fill the field'}
    return Response(message, status=status.HTTP_400_BAD_REQUEST)
  try:
    logger.warning(data['username'])
    user = User.objects.get(userName=data['username'])
    logger.warning('hi')
    if user.email != data['email']:
      logger.warning('hello')
      message={'message': 'Email does not match'}
      return Response(message, status=status.HTTP_400_BAD_REQUEST)
  except Exception as e:
    message = {'message': str(e)}
    return Response(message, status=status.HTTP_404_NOT_FOUND)
  email = [user.email]
  subject = "Password"
  body = f"Dear {user.firstName}, \n\n A request has been received to send your current password to this email.\n \t\t  Current Password of your account is {user.password}. \n\n Thank you!"
  sendEmail(email, subject, body)
  message = {'message': 'Please Wait, your current password is sent to your email'}
  return Response(message, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def upgradeSemester(request):
  students = User.objects.filter(role=Roles.STUDENT)
  logger.warn(students)
  try:
    for student in students:
      logger.warning(student)
      # logger.warning(student.semester)
      logger.warning(student.semester.pk)
      if student.semester.pk != 8:
        logger.warning('hihi')
        upgrade_to = Semester.objects.get(pk=student.semester.pk+1)
        student.semester = upgrade_to
        student.save() 
        logger.warning(student.semester.pk)
  except Exception as e:
    logger.warning(e)
  message = {"message": "Semester Upgraded"}
  return Response(message, status=status.HTTP_200_OK)