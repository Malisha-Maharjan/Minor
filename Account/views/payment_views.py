import json
import logging

# from rest_framework_simplejwt.utils import 
import requests
from django.db import connection
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
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
@authentication_classes([])
@permission_classes([])
def transaction(request):
  data = json.loads(request.body)

  try:
    student = User.objects.get(userName=data['userName'])
    semester = Semester.objects.get(pk=data['semester'])
    # serializer = TransactionSerializer(data=request.data)
    email = []
    # if serializer.is_valid():
    logger.warning('hi payment')
    transaction = Transaction(
    user = student,
    semester = semester,
    faculty = student.faculty,
    type = data['type'],
    amount = data['amount'])
    transaction.save()
    email.append(student.email)
    # sendEmail(email)
    message={}
    if transaction.type == 1:
      message={"message": "Bill is added"}
    else:
      message={"message": "Bill is paid"}
    return Response(message, status=status.HTTP_200_OK)
  except Exception as e:
    logger.warning(e)
    error = {"error": str(e)}
    return Response(error, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def khaltiVerify(request):
  try:
    data = json.loads(request.body) 
    logger.warning('khalti payment')
    url = KHALTI_VERIFY_URL
    payload = {
      'token': data['token'],
      'amount': data['amount']
    }
    logger.warning(data)
    username = data['userName']
    semester = Semester.objects.get(pk=data['semester'])

    logger.warning(payload)
    headers = {
      'Authorization': KHALTI_SECRET_KEY
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    logger.warning(response)
    logger.warning(response.status_code)
    email=[]
    if response.status_code == 200:
      logger.warning('inside ok')
      student = User.objects.get(userName=username)
      logger.warning(student)
      transaction = Transaction(
          user = student,
          type = 2,
          amount = data['amount']/100,
          semester = semester,
          faculty = student.faculty)
      transaction.save()
      email.append(student.email)
      sendEmail(email)
      message={'message': 'Bill paid via Khalti'}
      return Response(message, status=status.HTTP_200_OK)
    message = {'message': 'Invalid data'}   
    return Response(message, status=status.HTTP_400_BAD_REQUEST)
  except Exception as e:
    error = {"error": str(e)}
    return Response(error, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def due(request, username):
  try:
    user = User.objects.get(userName=username)
  except Exception as e:
    error = {"error": str(e)}
    return Response(error, status=status.HTTP_404_NOT_FOUND)
  billDetail = []
  try:
    semester = Semester.objects.get(pk=user.semester.pk)
    for i in range(1, user.semester.pk + 1):
      logger.warning('hi')
      bill = Transaction.objects.filter(user__userName=username, type=1, semester__pk=i).aggregate(bill_sum=Sum('amount'))
      paid = Transaction.objects.filter(user__userName=username, type=2, semester__pk=i).aggregate(paid_sum=Sum('amount'))
      scholarship = Transaction.objects.filter(user__userName=username, type=3, semester__pk=i).aggregate(scholarship_sum=Sum('amount'))
      if scholarship['scholarship_sum'] == None or bill['bill_sum'] == None or paid['paid_sum'] == None:
        scholarship['scholarship_sum'] = 0 
        bill['bill_sum'] = 0
        paid['paid_sum'] = 0
      item={}
      item['semester'] = i
      item['bill'] = bill['bill_sum']
      item['paid'] = paid['paid_sum']
      item['scholarship'] = scholarship['scholarship_sum']
      item['due'] = bill['bill_sum'] - paid['paid_sum'] + scholarship['scholarship_sum']
      billDetail.append(item)
      logger.warning(i)
  except Exception as e:
    error = {"error": str(e)}
    return Response(error, status=status.HTTP_404_NOT_FOUND)
  return JsonResponse(list(billDetail), safe=False)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def StudentPaymentDetails(request, username):
  try :
    user = User.objects.get(userName=username)
    serializer = UserStudentTransactionSerializer(user)
    logger.warning(serializer.data)
    return Response(serializer.data)
  except Exception as e:
    error = {"error": str(e)}
    return Response(error, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
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
@authentication_classes([])
@permission_classes([])
def bulkBillAdd(request):
  try: 
    data = json.loads(request.body)
    batch = data['batch']
    amount = data['amount']
    faculty = data['faculty']
    students = User.objects.filter(batch=batch, faculty=faculty)
    logger.warning(students)
    if students == None:
      message = {"message": "User not found"}
      return Response(message)
    transaction=[]
    email=[]
    for student in students:
      transaction.append(Transaction(
        user = student,
        type = 1,
        amount = amount,
        semester = student.semester,
        faculty = student.faculty
      ))
      email.append(student.email)
      # sendEmail(student.student)
  except Exception as e:
    logger.warning(e)
    return Response("exception")
  # sendEmail(email)
  Transaction.objects.bulk_create(transaction)
  return Response("ok")




