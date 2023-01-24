from django.db import models


class Roles(object):
  ADMIN = 1
  STAFF = 2
  STUDENT = 3

class TransactionsTypes(object):
  BILL = 1
  PAYMENT = 2
class User(models.Model):
  userName = models.CharField(max_length=100, unique=True)
  firstName = models.CharField(max_length=100)
  lastName = models.CharField(max_length=100)
  password = models.CharField(max_length=100)
  role = models.IntegerField()
  email = models.EmailField(default='malishamaharjan00@gmail.com')

  def __str__(self):
    return f'{self.userName} has role{self.role}'
  
class Student(models.Model):
  student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student")
  faculty = models.CharField(max_length=5)
  batch = models.CharField(max_length=5)
  semester = models.IntegerField()
  totalFee = models.FloatField()
  
# # # payment model
class Transaction(models.Model):
  transaction = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="transaction")
  type = models.IntegerField(null=True, default=TransactionsTypes.PAYMENT)
  amount = models.FloatField(null=True, default=0)

# f'select * from User where role = {Roles.STUDENT}
#query ma garni minus

# class Image(models.Model):
#   image = models.ImageField(upload_to=,)