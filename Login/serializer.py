from rest_framework import serializers

from Login.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta: 
      model = User
      fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Student
    fields = "__all__"


