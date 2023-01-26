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


class TransactionDetailSerializer(serializers.ModelSerializer):
  class Meta:
    model = Transaction 
    fields = ['type', 'amount', 'semester']

class UserStudentTransactionSerializer(serializers.ModelSerializer):
  transaction = TransactionDetailSerializer(many=True)
  class Meta:
    model = User
    fields = ['userName', 'firstName', 'lastName', 'faculty', 'batch', 'transaction']


# class ImageSerializer(serializers.ModelSerializer):
#   class Meta:
#     model = imageModel
#     fields = '__all__'

# class FirstSemesterSerializer(serializers.ModelSerializer):
#   class Meta:
#     model = FirstSemester
#     fields = ['mathematicsI','computer_Programming', 'engineering_DrawingI','engineering_Physics', 'applied_Mechanics', 'basic_Electrical_Engineering', 'total_Marks','percentage']

# class SecondSemesterSerializer(serializers.ModelSerializer):
#   class Meta:
#     model = FirstSemester
#     fields = ['mathematicsII', 'engineering_DrawingII', 'basic_Electronics_Engineering', 'engineering_Chemistry', 'thermodynamics', 'workshop', 'total_Marks', 'percentage']