import json
import logging

import jwt
from django.forms.models import model_to_dict
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.response import Response

from ..models import *
from ..serializer import *

logger = logging.getLogger(__name__)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def addMark(request, username):
  marks = json.loads(request.body)
  try: 
    student = User.objects.get(userName=username)
    semester = Semester.objects.get(pk=marks['semester'])
    subject = Subject.objects.get(pk=marks['subject'], semester__pk=marks['semester'])
    result = Marks(
      student = student,
      semester = semester,
      subject = subject,
      marks = marks['marks']
    )
    logger.warning(result)
    result.save()
    message = {"message": "Mark added"}
    return Response(message)
  except Exception as e:
    logger.warning(e)
    error = {"message": str(e)}
    return Response(error, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def getMark(request, username, id):
  pass
  try:
    student = User.objects.get(userName=username)
    # mark = Marks.objects.filter(semester__pk = id, student__pk = student.pk).select_related('subject')
    # serializer = MarksSerializer(mark, many=True)
    # return Response(serializer.data)
    marks = Marks.objects.filter(semester__pk = id, student__pk = student.pk).select_related().all()
    result = []
    for mark in marks:
      item = model_to_dict(mark.subject, fields=['subject', 'pass_marks'])
      item['marks'] = mark.marks
      result.append(item)
    return JsonResponse(list(result), safe=False)
  except Exception as e:
    logger.warning(e)
    message = {"message": "User not found"}
    return Response(message)
