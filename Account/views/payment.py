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

from backend.settings import DATABASES, KHALTI_SECRET_KEY, KHALTI_VERIFY_URL

from ..models import *
from ..send_email import *
from ..serializer import *

logger = logging.getLogger(__name__)

@api_view(['POST'])
def transaction(request, username):
  try:
    student = User.objects.get(userName=username)
    serializer = TransactionSerializer(data=request.data)
    email = []
    if serializer.is_valid():
      logger.warning('hi payment')
      transaction = Transaction(
        user = student,
        semester = student.semester,
        type = serializer.data['type'],
        amount = serializer.data['amount'])
      transaction.save()
      email.append(student.email)
      sendEmail(email)
      message={}
      if transaction.type == 1:
        message={"message": "Bill is added"}
      else:
        message={"message": "Bill is paid"}
      return Response(message, status=status.HTTP_200_OK)
  except Exception as e:
    logger.warning(e)
    return Response('exception')
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
  username = data['userName']

  logger.warning(payload)
  headers = {
    'Authorization': KHALTI_SECRET_KEY
  }
  response = requests.request("POST", url, headers=headers, data=payload)
  logger.warning(response)
  logger.warning(response.status_code)
  email=[]
  if response.status_code == 200:
    student = User.objects.get(student__userName=username, is_active=True)
    transaction = Transaction(
        user = student,
        type = 2,
        amount = data['amount']/1000,
        semester = student.semester)
    transaction.save()
    email.append(student.email)
    sendEmail(email)
    message={'message': 'Bill paid via Khalti'}
    return Response(message, status=status.HTTP_200_OK)
  message = {'message': 'Invalid data'}   
  return Response(message, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def due(request, username):
  bill = Transaction.objects.filter(user__userName=username, type=1).aggregate(bill_sum=Sum('amount'))
  paid = Transaction.objects.filter(user__userName=username, type=2).aggregate(paid_sum=Sum('amount'))
  scholarship = Transaction.objects.filter(user__userName=username, type=3).aggregate(scholarship_sum=Sum('amount'))
  if scholarship['scholarship_sum'] == None:
    scholarship['scholarship_sum'] = 0 
  due = bill['bill_sum'] - paid['paid_sum'] + scholarship['scholarship_sum']
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
def upgradeSemester(request):
  data = json.loads(request.body)
  batch = data['batch']
  faculty = data['faculty']
  students = User.objects.filter(batch=batch, faculty=faculty)
  current_semester = students.first().semester.pk
  if current_semester==8:
    return Response("invalid upgrade", status=status.HTTP_400_BAD_REQUEST)
  upgrade_to = Semester.objects.get(pk=current_semester+1)
  try:
    for student in students:
      student.semester = upgrade_to
      student.save() 
  except Exception as e:
    logger.warning(e)
  return Response("ok")

@api_view(['POST'])
def bulkBillAdd(request):
  data = json.loads(request.body)
  batch = data['batch']
  amount = data['amount']
  faculty = data['faculty']
  students = User.objects.filter(batch=batch, faculty=faculty)
  transaction=[]
  email=[]
  for student in students:
    transaction.append(Transaction(
      user = student,
      type = 1,
      amount = amount,
      semester = student.semester
    ))
    email.append(student.email)
    # sendEmail(student.student)
  # sendEmail(email)
  Transaction.objects.bulk_create(transaction)
  return Response("ok")




