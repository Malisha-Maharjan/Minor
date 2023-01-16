from django.db import models


class Roles(object):
  ADMIN = 1
  STAFF = 2
  STUDENT = 3

class User(models.Model):
  userName = models.CharField(max_length=100, unique=True)
  firstName = models.CharField(max_length=100)
  lastName = models.CharField(max_length=100)
  password = models.CharField(max_length=100)
  role = models.IntegerField()

  def __str__(self):
    return f'{self.userName} has {self.role}'
  
class Student(models.Model):
  student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student")
  totalFee = models.FloatField()
  # admissionFee = models.FloatField(default=1)
  # firstSem = models.FloatField()
  # secondSem = models.FloatField()
  # thirdSem = models.FloatField()
  # fourthSem = models.FloatField()
  # fifthSem = models.FloatField()
  # sixthSem = models.FloatField()
  # seventhSem = models.FloatField()
  # eighthSem = models.FloatField()
  # scholarship = models.FloatField(null=True)
  
# # payment model
class Transaction(models.Model):
  student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student_transaction")
  transaction = models.FloatField()

# f'select * from User where role = {Roles.STUDENT}
#query ma garni minus