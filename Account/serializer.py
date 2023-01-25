from Account.models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
  class Meta: 
    model = User
    fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Transaction 
    fields = ['type', 'amount']

class StudentTransactionSerializer(serializers.ModelSerializer):
  # user = UserSerializer(many=True)
  # student = StudentSerializer(many=True)
  # user =  UserSerializer()
  transaction = TransactionSerializer(many=True)
  class Meta:
    model = Semester
    fields = ['std_semester', 'transaction']

class UserStudentTransactionSerializer(serializers.ModelSerializer):
  # transaction = StudentTransactionSerializer(many=True)
  student = StudentTransactionSerializer(many=True)
  class Meta:
    model = User
    fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
  class Meta:
    model = imageModel
    fields = '__all__'