import logging

from django.db import connection
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .serializer import UserSerializer

logger = logging.getLogger(__name__)
cursor=connection.cursor()

# Create your views here.
@api_view(['POST'])
def studentRegister(request):
  message=""
  serializer = UserSerializer(data=request.data)

  if serializer.is_valid():
    user = User(
      userName=serializer.data['userName'],
      firstName=serializer.data['firstName'],
      lastName=serializer.data['lastName'],
      role=3,
    )
    user.save()
    message = "true"
    logger.warning(serializer.data['role'])
    return Response(message, status=status.HTTP_200_OK)
  message = "false"
  return Response(message, status=status.HTTP_400_BAD_REQUEST)
# select * from users where username='' and passeord = ''

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

# @api_view(['POST'])
# def payment(request):
