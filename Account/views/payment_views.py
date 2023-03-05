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
  logger.warning(data)
  try:
    student = User.objects.get(userName=data['userName'])
    logger.warning(student.semester.id)
    logger.warning(data['semester'])
    logger.warning(data['semester'] > student.semester.id)
    if data['semester'] > student.semester.id:
      logger.warning("exception")
      raise Exception()
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

    if transaction.type == TransactionsTypes.PAYMENT:
      subject = "Bill Update: Payment Received"
      body = f"Dear {student.firstName}, \n\n I hope this email finds you in good health and spirits. I am writing to confirm that we have received your payment for the recent bill i.e. Rs{data['amount']}. I am pleased to inform you that the payment was successful and has been processed."

    if transaction.type == TransactionsTypes.BILL:
      subject = "Billing Statement"
      body = f"Dear {student.firstName}, \n\nI hope this email finds you well. I am writing to inform you that a new bill has been added to your account. The details of the bill are as follows:\nAmount Due: Rs{data['amount']} \nPlease take a moment to review the billing statement and let us know if you have any questions or concerns. We are here to help and would be happy to assist you in any way possible."
    
    if transaction.type == TransactionsTypes.SCHOLARSHIP:
      subject = "Scholarship Awarded"
      body = f"Dear {student.firstName},\n I hope this email finds you in good health and spirits. I am writing to inform you that you have been awarded a scholarship worth Rs{data['amount']}. This scholarship is awarded to you on the basis of merit list."

    sendEmail(email, subject, body)
    message={}
    if transaction.type == TransactionsTypes.BILL:
      message={"message": "Bill is added"}
    if transaction.type == TransactionsTypes.PAYMENT:
      message={"message": "Bill is paid"}
    if transaction.type == TransactionsTypes.SCHOLARSHIP:
      message = {'message': "Scholarship is awarded"}
    return Response(message, status=status.HTTP_200_OK)

  except Exception as e:
    logger.warning(e)
    error = {"message": "Error: Operation unsuccessful"}
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
      subject = "Bill Update: Payment Received via Khalti"
      body = f"Dear {student.firstName}, \n\n I hope this email finds you in good health and spirits. I am writing to confirm that we have received your payment for the recent bill i.e. Rs{data['amount']} via khalti. I am pleased to inform you that the payment was successful and has been processed."
      sendEmail(email, subject, body)
      message={'message': 'Bill paid via Khalti'}
      return Response(message, status=status.HTTP_200_OK)
    message = {'message': 'Invalid data'}   
    return Response(message, status=status.HTTP_400_BAD_REQUEST)
  except Exception as e:
    error = {"message": str(e)}
    logger.warning(e)
    return Response(error, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def due(request, username):
  try:
    logger.warning(username)
    user = User.objects.get(userName=username)
  except Exception as e:
    error = {"message": 'Error: User not found'}
    return Response(error, status=status.HTTP_404_NOT_FOUND)
  billDetail = []
  try:
    semester = Semester.objects.get(pk=user.semester.pk)
    logger.warning(semester)
    for i in range(1, user.semester.pk + 1):
      bill = Transaction.objects.filter(user__userName=username, type=1, semester__pk=i).aggregate(bill_sum=Sum('amount'))
      paid = Transaction.objects.filter(user__userName=username, type=2, semester__pk=i).aggregate(paid_sum=Sum('amount'))
      scholarship = Transaction.objects.filter(user__userName=username, type=3, semester__pk=i).aggregate(scholarship_sum=Sum('amount'))
      if scholarship['scholarship_sum'] == None:
        scholarship['scholarship_sum'] = 0
      if  bill['bill_sum'] == None: 
        bill['bill_sum'] = 0
      if paid['paid_sum'] == None:
        paid['paid_sum'] = 0
      item={}
      item['semester'] = i
      item['bill'] = bill['bill_sum']
      item['paid'] = paid['paid_sum']
      item['scholarship'] = scholarship['scholarship_sum']
      item['due'] = bill['bill_sum'] - paid['paid_sum']- scholarship['scholarship_sum']
      billDetail.append(item)
      logger.warning(i)
  except Exception as e:
    error = {"message": str(e)}
    return Response(error, status=status.HTTP_404_NOT_FOUND)
  return JsonResponse(list(billDetail), safe=False)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def StudentPaymentDetails(request, username):
  try :
    user = User.objects.get(userName=username)
    # serializer = UserStudentTransactionSerializer(user)
    # logger.warning(serializer.data)
    # return Response(serializer.data)
    transaction = Transaction.objects.filter(user = user.pk)
    serializer = TransactionDetailSerializer(transaction, many=True)
    return Response(serializer.data)
  except Exception as e:
    logger.warning(e)
    error = {"message": "Error: User not found"}
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
    message = {"message": "Error: Invalid upgrade"}
    return Response(message, status=status.HTTP_400_BAD_REQUEST)
  upgrade_to = Semester.objects.get(pk=current_semester+1)
  try:
    for student in students:
      student.semester = upgrade_to
      student.save() 
  except Exception as e:
    logger.warning(e)
  message = {"message": "Semester Upgraded"}
  return Response(message, status=status.HTTP_200_OK)

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
      return Response(message, status=status.HTTP_404_NOT_FOUND)
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




