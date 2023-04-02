import json
import logging

from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.response import Response

from ...models import *
from ...send_email import *
from ...serializer import *

logger = logging.getLogger(__name__)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def transaction(request):
  data = json.loads(request.body)
  logger.warning(data)
  if data['amount'] == None or len(data['userName']) == 0 or data['semester'] == None:
    message = {'message': 'Please fill all the fields'}
    return Response(message, status=status.HTTP_400_BAD_REQUEST)
  try:
    student = User.objects.get(userName=data['userName'])
    logger.warning(student.semester.pk)
    logger.warning(data['semester'])
    logger.warning(data['semester'] > student.semester.pk)
    if data['semester'] > student.semester.pk:
      logger.warning("exception")
      message = 'Invalid Semester'
      raise Exception()
    semester = Semester.objects.get(pk=data['semester'])
    # serializer = TransactionSerializer(data=request.data)
    email = []
    # if serializer.is_valid():
    logger.warning('hi payment')
    due = getDue(student.userName, semester.pk)
    if due['due'] < data['amount']:
      message = {"message": f"The amount you entered exceeds the due limit. Your due is Rs.{due['due']}."}
      return Response(message)
    transaction = Transaction(
    user = student,
    semester = semester,
    faculty = student.faculty,
    type = data['type'],
    amount = data['amount'])
    logger.warning(due)
    transaction.save()
    email.append(student.email)

    if transaction.type == TransactionsTypes.PAYMENT:
      subject = "Bill Update: Payment Received"
      body = f"Dear {student.firstName}, \n\n I hope this email finds you in good health and spirits. I am writing to confirm that we have received your payment for the recent bill i.e. Rs{data['amount']}. I am pleased to inform you that the payment was successful and has been processed.\n Best Regards, \n Student Portal"

    if transaction.type == TransactionsTypes.BILL:
      subject = "Billing Statement"
      body = f"Dear {student.firstName}, \n\nI hope this email finds you well. I am writing to inform you that a new bill has been added to your account. The details of the bill are as follows:\nAmount Added: Rs{data['amount']} \nPlease take a moment to review the billing statement and let us know if you have any questions or concerns. We are here to help and would be happy to assist you in any way possible. \n Best Regards, \n Student Portal"
    
    if transaction.type == TransactionsTypes.SCHOLARSHIP:
      subject = "Scholarship Awarded"
      body = f"Dear {student.firstName},\n I hope this email finds you in good health and spirits. I am writing to inform you that you have been awarded a scholarship worth Rs{data['amount']}. This scholarship is awarded to you on the basis of merit list. \n Best Regards, \n Student Portal"
    transaction = Transaction(
    user = student,
    semester = semester,
    faculty = student.faculty,
    type = data['type'],
    amount = data['amount'])
    logger.warning(due)
    transaction.save()
    email.append(student.email)
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
    error = {"message": message}
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
      # bill = Transaction.objects.filter(user__userName=username, type=TransactionsTypes.BILL, semester__pk=i).aggregate(bill_sum=Sum('amount'))
      # paid = Transaction.objects.filter(user__userName=username, type=TransactionsTypes.PAYMENT, semester__pk=i).aggregate(paid_sum=Sum('amount'))
      # scholarship = Transaction.objects.filter(user__userName=username, type=TransactionsTypes.SCHOLARSHIP, semester__pk=i).aggregate(scholarship_sum=Sum('amount'))
      # if scholarship['scholarship_sum'] == None:
      #   scholarship['scholarship_sum'] = 0
      # if  bill['bill_sum'] == None: 
      #   bill['bill_sum'] = 0
      # if paid['paid_sum'] == None:
      #   paid['paid_sum'] = 0
      # item={}
      # item['semester'] = i
      # item['bill'] = bill['bill_sum']
      # item['paid'] = paid['paid_sum']
      # item['scholarship'] = scholarship['scholarship_sum']
      # item['due'] = bill['bill_sum'] - paid['paid_sum']- scholarship['scholarship_sum']
      item = getDue(username, i)
      if item['due'] != 0:
        billDetail.append(item)
      logger.warning(i)
  except Exception as e:
    error = {"message": str(e)}
    return Response(error, status=status.HTTP_404_NOT_FOUND)
  return JsonResponse(list(billDetail), safe=False)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def semesterDue(request, username, semester):
  logger.warning('hi due')
  logger.warning(semester)
  result = getDue(username, semester)
  due = {'due': result['due']}
  return Response(due, status=status.HTTP_200_OK)


def getDue(username, semester):
    bill = Transaction.objects.filter(user__userName=username, type=TransactionsTypes.BILL, semester__pk=semester).aggregate(bill_sum=Sum('amount'))
    paid = Transaction.objects.filter(user__userName=username, type=TransactionsTypes.PAYMENT, semester__pk=semester).aggregate(paid_sum=Sum('amount'))
    scholarship = Transaction.objects.filter(user__userName=username, type=TransactionsTypes.SCHOLARSHIP, semester__pk=semester).aggregate(scholarship_sum=Sum('amount'))
    if scholarship['scholarship_sum'] == None:
      scholarship['scholarship_sum'] = 0
    if  bill['bill_sum'] == None: 
      bill['bill_sum'] = 0
    if paid['paid_sum'] == None:
      paid['paid_sum'] = 0
    item={}
    item['semester'] = semester
    item['bill'] = bill['bill_sum']
    item['paid'] = paid['paid_sum']
    item['scholarship'] = scholarship['scholarship_sum']
    item['due'] = bill['bill_sum'] - paid['paid_sum']- scholarship['scholarship_sum']
    return item

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
def bulkBillAdd(request):
  logger.warning('i am bulk entries')
  try: 
    data = json.loads(request.body)
    batch = data['batch']
    amount = data['amount']
    faculty = data['faculty']
    students = User.objects.filter(batch=batch, faculty=faculty)
    logger.warning(students)
    if students == None:
      message = {"message": "User not found"}
      return Response(message, status=status.HTTP_400_BAD_REQUEST)
    transaction=[]
    email=[]
    for student in students:
      transaction.append(Transaction(
        user = student,
        type = TransactionsTypes.BILL,
        amount = amount,
        semester = student.semester,
        faculty = student.faculty
      ))
      email.append(student.email)
  except Exception as e:
    logger.warning(e)
    message = {'message': 'Invalid Data'}
    return Response(message,  status=status.HTTP_404_NOT_FOUND)
  subject = "Billing Statement"
  body = f"Dear student, \n\nI hope this email finds you well. I am writing to inform you that a new bill has been added to your account. The details of the bill are as follows:\nAmount Added: Rs{data['amount']} \nPlease take a moment to review the billing statement and let us know if you have any questions or concerns. We are here to help and would be happy to assist you in any way possible. \n Best Regards, \n LEC"
  sendEmail(email, subject, body)
  Transaction.objects.bulk_create(transaction)
  message = {"message": f"Bills have been added to the all students of {batch} batch"}
  return Response(message, status=status.HTTP_200_OK)