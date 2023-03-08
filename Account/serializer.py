from rest_framework import serializers

from Account.models import *


class SemesterSerializer(serializers.ModelSerializer):
  class Meta:
    model = Semester
    fields = '__all__'

class FacultySerializer(serializers.ModelSerializer):
  class Meta:
    model =  Faculty
    fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
  class Meta: 
    model = User
    fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Transaction 
    fields = ['type', 'amount']


class TransactionDetailSerializer(serializers.ModelSerializer):
  semester = SemesterSerializer()
  class Meta:
    model = Transaction 
    fields = ['type', 'amount', 'date', 'semester']

class UserStudentTransactionSerializer(serializers.ModelSerializer):
  transaction = TransactionDetailSerializer(many=True)
  class Meta:
    model = User
    fields = ['transaction']

class SubjectSerializer(serializers.ModelSerializer):
  class Meta:
    model = Subject
    fields = '__all__'

class MarksSerializer(serializers.ModelSerializer):
  class Meta:
    model = Marks
    fields = ['marks', 'subject']

# class ResultSerializer(serializers.ModelSerializer):
#   student_mark = MarksSerializer(many=True)
#   class Meta:
#     model = Marks
#     fields = ['userName', 'student_mark']

# class SemesterMarksSerializer(serializers.ModelSerializer):
#   student_mark = MA
#   class Meta:


