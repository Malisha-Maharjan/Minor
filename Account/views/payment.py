import json
import logging

# from rest_framework_simplejwt.utils import 
import requests
from django.db import connection
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.response import Response

from backend.settings import KHALTI_SECRET_KEY, KHALTI_VERIFY_URL

from ..models import *
from ..serializer import *

logger = logging.getLogger(__name__)
cursor=connection.cursor()

@api_view(['POST'])
def manualPayment(request, username):
  user = User.objects.get(userName=username)
  serializer = ManualPaymentSerializer(data=request.data)
  if serializer.is_valid():
    logger.warning('hi payment')
    payment = Transaction(
      student = user,
      transaction = serializer.data['transaction'])
    payment.save()
    return Response('true', status=status.HTTP_200_OK)
  return Response('false', status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def khaltiVerify(request):
  data = json.loads(request.body) 
  url = KHALTI_VERIFY_URL
  payload = {
    'token': data['token'],
    'amount': data['amount']
  }

  logger.warning(payload)
  headers = {
    'Authorization': KHALTI_SECRET_KEY
  }
  response = requests.request("POST", url, headers=headers, data=payload)
  logger.warning(response)

  return Response()
  
@api_view(['GET'])
def due(request, username):
  payments = Transaction.objects.filter(student__userName = username)
  student = Student.objects.get(student__userName = username)
  due = student.totalFee
  for payment in payments: 
    due = due - payment.transaction
  message = {'due': due}
  return Response(message)
