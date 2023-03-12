import json
import logging

from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.response import Response

from ...models import *
from ...send_email import *
from ...serializer import *
from .transaction_view import getDue

logger = logging.getLogger(__name__)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def addVoucher(request):
  logger.warning('hi i am voucher')
  data = json.loads(request.body)
  logger.warning(data)
  try: 
    student = User.objects.get(userName = data['username'])
    semester = Semester.objects.get(pk=data['semester'])
    voucher = Voucher(
      student = student,
      semester = semester,
      faculty = student.faculty,
      amount = data['amount'],
      image = data['image']
    )
    voucher.save()
  except Exception as e:
    logger.warning(e)
    message = {'message': str(e)}
    return Response(message)
  message = {"message": f"Voucher Uploaded. You will receive an email after your payment is verified"}
  return Response(message)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def unverifiedVoucher(request):
  vouchers = Voucher.objects.filter(is_verified=False).select_related().all()
  result = []
  for voucher in vouchers:
    item = model_to_dict(voucher.student, fields=['userName'])
    item['amount'] = voucher.amount
    item['semester'] = voucher.semester.name
    item['faculty'] = voucher.faculty.name
    item['date'] = voucher.date
    item['voucher_id'] = voucher.pk
    item['image'] = voucher.image
    result.append(item)
  return JsonResponse(list(result), safe=False) 

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def verifyVoucher(request):
  try:
    data = json.loads(request.body)
    voucher = Voucher.objects.get(pk=data['voucher_id'])
    logger.warning(data)
    if not data['validity']:
      message = {"message": "Voucher not verified"}
      subject = "Voucher Not Verified"
      body = f"Dear {voucher.student.firstName}, \n\n Your payment through voucher has not been verified. Please visit the college premises.\n\n Best Regards, \n Student Portal"
      email = [voucher.student.email]
      voucher.delete()
      sendEmail(email, subject, body)
      return Response(message)
    due = getDue(voucher.student.userName, voucher.semester.pk)
    if due['due'] < voucher.amount:
      message = {"message": f"The amount of this voucher entered exceeds the due limit. The due is Rs{due['due']}."}
      subject = "Payment via Voucher exceeds the due amount"
      body = f"Dear {voucher.student.firstName}, \n\n Your payment through voucher has exceeds the current due amount of this semester. The due amount is {due['due']}. Please visit the college premises for further processing.\n\n Best Regards, \n Student Portal"
      email = [voucher.student.email]
      sendEmail(email, subject, body)
      return Response(message)
    voucher.is_verified = True
    transaction = Transaction(
    user = voucher.student,
    semester = voucher.semester,
    faculty = voucher.faculty,
    type = TransactionsTypes.PAYMENT,
    amount = voucher.amount
    )
    subject = "Voucher Verification: Payment Received"
    body = f"Dear {voucher.student.firstName}, \n\n Your payment through voucher has been verified. \n Amount: {voucher.amount} has been received\n\n Best regards, \n Student Portal"
    email = [voucher.student.email]
    sendEmail(email, subject, body)
    voucher.save()
    transaction.save()
    message = {"message": "Voucher Verified."}
    return Response(message)
  except Exception as e:
    message = {"message": str(e)}
    return Response(message)
