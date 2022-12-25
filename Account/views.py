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
    serializer.save()
    message = "Data is posted"
    return Response(message, status=status.HTTP_200_OK)
  message = str(serializer.error_messages)
  return Response(message, status=status.HTTP_400_BAD_REQUEST)
# select * from users where username='' and passeord = ''

@api_view(['GET'])
def getInfo(request):
  student = User.objects.all()
  serializer = UserSerializer(student, many=True)
  return Response(serializer.data)

