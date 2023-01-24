import json
import logging

# from rest_framework_simplejwt.utils import 
import requests
from django.db import connection
from django.db.models import Sum
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.response import Response

from backend.settings import KHALTI_SECRET_KEY, KHALTI_VERIFY_URL

from ..models import *
from ..send_email import *
from ..serializer import *

logger = logging.getLogger(__name__)
cursor=connection.cursor()

@api_view(['POST'])
def transaction(request, username):
  student = Student.objects.get(student__userName=username)
  serializer = TransactionSerializer(data=request.data)
  if serializer.is_valid():
    logger.warning('hi payment')
    transaction = Transaction(
      transaction = student,
      type = serializer.data['type'],
      amount = serializer.data['amount'])
    transaction.save()
    sendEmail(student.student)
    message={}
    if transaction.type == 1:
      message={"message": "Bill is added"}
    else:
      message={"message": "Bill is paid"}
    return Response(message, status=status.HTTP_200_OK)
  return Response(message, status=status.HTTP_400_BAD_REQUEST)

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
  if response == 200:
    logger.warning(response)
  return Response()

@api_view(['GET'])
def due(request, username):

  bill = Transaction.objects.filter(transaction__student__userName=username, type=1).aggregate(bill_sum=Sum('amount'))
  paid = Transaction.objects.filter(transaction__student__userName=username, type=2).aggregate(paid_sum=Sum('amount'))
  due = bill['bill_sum'] - paid['paid_sum']
  message={'due': due}
  return Response(message)

@api_view(['GET'])
def StudentPaymentDetails(request, username):
  user = User.objects.get(userName=username)
  serializer = UserStudentTransactionSerializer(user)
  try :
    logger.warning(serializer.data)
    return Response(serializer.data)
  except Exception as e:
    logger.warning(e)
    return Response('exception')

@api_view(['POST'])
def semesterFee(request, semester):
  pass