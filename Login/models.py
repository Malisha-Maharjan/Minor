from django.db import models


class User(models.Model):
  username = models.CharField(max_length=100, unique=True)
  firstName = models.CharField(max_length=100)
  lastName = models.CharField(max_length=100)
  password = models.CharField(max_length=100)
  # role = models.IntegerField(max_length=20, default="User")
  


class Student(User):
  fees = models.FloatField()


# class Roles(object):
#   ADMIN = 1
#   STAFF = 2
#   STUDENT = 3


