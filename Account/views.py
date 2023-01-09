import json
import logging

# from rest_framework_simplejwt.utils import 
import jwt
from django.db import connection
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from backend.settings import SIMPLE_JWT

from .models import *
from .serializer import *

logger = logging.getLogger(__name__)
cursor=connection.cursor()

def validate_token(request):
  token = request.headers.get('Authorization')
  if token:
    if token:
      logger.warning('inside token')
      payload =  jwt.decode(
      token,
      SIMPLE_JWT['SIGNING_KEY'],
      algorithms=[SIMPLE_JWT['ALGORITHM']],
)
  return payload

@api_view(['POST'])
def studentRegister(request):
  message=""
  userSerializer = UserSerializer(data=request.data)
  payload = validate_token(request)
  if payload['role'] == 1:
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
  message = {'message': "Unauthorized access"}
  return Response(message)
# select * from users where username='' and password = ''

@api_view(['GET'])
def getAllInfo(request):
  student = User.objects.all()
  serializer = UserSerializer(student, many=True)
  return Response(serializer.data)

@api_view(['GET'])
def getInfo(request, id):
  student = User.objects.get(pk=id)
  serializer = UserSerializer(student)
  return Response(serializer.data)

@api_view(['PUT'])
def updateInfo(request, id):
  user = User.objects.get(pk=id)
  serializer = UserSerializer(user, data=request.data)
  if serializer.is_valid():
    serializer.save()
    return Response("true", status=status.HTTP_200_OK)
  return Response("false", status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
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
    data = {'access': str(access)}
    logger.warning(user.userName)
    return Response(data, status=status.HTTP_200_OK)
  except Exception as e:
    return Response('false', status=status.HTTP_401_UNAUTHORIZED)

# @api_view(['POST'])
# def payment(request, id):
#   user = User.objects.get(pk=id)
#   paymentSerializer = PaymentSerializer(data=request.data)
#   if paymentSerializer.is_valid():
#     payment = Payment(payment=paymentSerializer['payment'])
#     payment.student = user
#     user.totalFee = user.totalFee - payment.payment
#     payment.save()
#     return Response('true', status=status.HTTP_200_OK)
#   return Response('false', status=status.HTTP_400_BAD_REQUEST)