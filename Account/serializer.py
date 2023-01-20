from Account.models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
  class Meta: 
    model = User
    fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
  class Meta: 
    model = Student
    fields = ['totalFee']

class ManualPaymentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Transaction
    fields = ['transaction']

class StudentDetailsSerializer(serializers.ModelSerializer):
  student = StudentSerializer(many=True)
  class Meta:
    model = User
    fields = '__all__'
# class ScholarshipSerializer(serializers.ModelSerializer):
#   class Meta:
#     model = Scholarship
#     fields = '__all__'


# class PaymentSerializer(serializers.ModelSerializer):
#   class Meta:
#     model = Payment
#     fields = ('payment')