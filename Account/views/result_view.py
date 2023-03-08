import json
import logging

import jwt
from django.db.models import Sum
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
def addMark(request, username, semester):
  logger.warning('inside mark')
  marks = json.loads(request.body)
  logger.warning(marks[0])
  try: 
    student = User.objects.get(userName=username)
    if student.semester.pk < semester:
      message = {'message': 'invalid data'}
      return Response(message, status=status.HTTP_400_BAD_REQUEST)
    semester = Semester.objects.get(pk=semester)
    # subjects = Subject.objects.filter(semester__pk=semester).first()
    # subject_id = subjects.pk
    for mark in marks:
      subject = Subject.objects.get(pk=mark['id'])
      result = Marks(
        student = student,
        semester = semester,
        subject = subject,
        marks = mark['mark'],
        faculty = student.faculty
      )
      result.save()
      message = {'message': 'marks added'}
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
      logger.warning(mark.subject.pk)
      item = model_to_dict(mark.subject, fields=['id','subject', 'pass_marks', 'full_marks'])
      item['marks'] = mark.marks
      result.append(item)
    return JsonResponse(list(result), safe=False)
  except Exception as e:
    logger.warning(e)
    message = {"message": "User not found"}
    return Response(message, status=status.HTTP_400_BAD_REQUEST)

import numpy as np


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def getGraph(request, username):
  logger.warning(username)
  try: 
    student = User.objects.get(userName=username)
    y_axis = []
    x_axis = []
    logger.warning(student)
    mark = Marks.objects.filter(student__userName=username).last()
    logger.warning(mark.semester.pk)
    for i in range(1, mark.semester.pk+1):
      total = 0
      mark = Marks.objects.filter(semester__pk=i).aggregate(total_sum=Sum('marks'))
      y_axis.append(mark['total_sum'])
      semester = Semester.objects.get(pk=i)
      x_axis.append(semester.name)
  except Exception as e:
    logger.warning(e)
  logger.warning(y_axis)
  logger.warning(x_axis)
  x = np.array(x_axis)
  y = np.array(y_axis)
  message = {'x': x, 'y': y}
  # plt.plot(x, y)
  # plt.show()

  return Response(message)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def updateMarks(request, username, semester):
  data = json.loads(request.body)
  student = User.objects.get(userName=username)
  semester = Semester.objects.get(pk=semester)
  marks = Marks.objects.filter(student__userName=username, semester__pk=semester.pk)
  logger.warning(marks)
  logger.warning(data)
  for mark in marks:
    logger.warning(mark.pk)
  for update in data:
    for mark in marks:
      if update['id'] == mark.pk:
        mark.marks = update['mark']
        mark.save(update_fields = ['marks'])
  message = {'message': 'Result updated'}
  return Response(message)


import os
import sys
from pathlib import Path

import joblib

dataFolder = Path(r'/Users/malisha/Desktop/model/Jupyter/prediction.joblib')
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def model(request, username):
  try:
    student = User.objects.get(userName=username)
    logger.warning(student.semester.pk)
    mark = Marks.objects.filter(semester__pk = 7, student__userName = username).first()
    if mark == None:
      message = {'message': 'Prediction is not available. Please wait until you get your 7th sem result.'}
      return Response(message)
  except Exception as e:
    logger.warning(e)
    return Response('Error')
  try: 
    data = []
    marks = Marks.objects.filter(student__userName = username)
    for mark in marks:
      if mark.marks < 32:
        data.append(0)
      else:
        data.append(1)
    loaded_model = joblib.load(dataFolder)

    logger.warning(data)
    value = loaded_model.predict([data])
    if value == 1:
      message = {'message': 'Prediction: You will pass your 8th semester.'}
    else:
      message = {'message': 'Prediction: You will fail your 8th semester'}
    logging.warning(value)
  except Exception as e:
    logger.warning(e)
  return Response(message)
