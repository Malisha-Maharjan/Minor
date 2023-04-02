import json
import logging

import requests
from django.db import connection
from django.db.models import Sum
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.response import Response

from backend.settings import DATABASES, KHALTI_SECRET_KEY, KHALTI_VERIFY_URL

from ...models import *
from ...send_email import *
from ...serializer import *

logger = logging.getLogger(__name__)

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
      body = f"Dear {student.firstName}, \n\n I hope this email finds you in good health and spirits. I am writing to confirm that we have received your payment for the recent bill i.e. Rs{data['amount']/100} via khalti. I am pleased to inform you that the payment was successful and has been processed. \n Best Regards, \n Student Portal"
      sendEmail(email, subject, body)
      message={'message': 'Bill paid via Khalti'}
      return Response(message, status=status.HTTP_200_OK)
    message = {'message': 'Invalid data'}   
    return Response(message, status=status.HTTP_400_BAD_REQUEST)
  except Exception as e:
    error = {"message": str(e)}
    logger.warning(e)
    return Response(error, status=status.HTTP_404_NOT_FOUND)