from Account.models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
  class Meta: 
    model = User
    fields = '__all__'

# class FeeSerializer(serializers.ModelSerializer):
#   class Meta: 
#     model = Fee
#     fields = '__all__'

# class ScholarshipSerializer(serializers.ModelSerializer):
#   class Meta:
#     model = Scholarship
#     fields = '__all__'
