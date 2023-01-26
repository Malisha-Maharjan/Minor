from django.db import models


class Roles(object):
  ADMIN = 1
  STAFF = 2
  STUDENT = 3

class TransactionsTypes(object):
  BILL = 1
  PAYMENT = 2
  SCHOLARSHIP = 3

class Semester(models.Model):
  name = models.CharField(max_length=10)

class User(models.Model):
  userName = models.CharField(max_length=100, unique=True)
  firstName = models.CharField(max_length=100)
  lastName = models.CharField(max_length=100)
  password = models.CharField(max_length=100)
  role = models.IntegerField()
  email = models.EmailField(null=True)
  faculty = models.CharField(max_length=5, null=True)
  batch = models.CharField(max_length=5, null=True)
  semester = models.ForeignKey(Semester, null=True, on_delete=models.DO_NOTHING)

  def __str__(self):
    return f'{self.userName} has role{self.role}'
  
# # # payment mod

class Transaction(models.Model):
  user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="transaction")
  semester = models.ForeignKey(Semester, null=True, on_delete=models.DO_NOTHING)
  type = models.IntegerField(null=True)
  amount = models.FloatField(null=True)
  date = models.DateTimeField(auto_now_add=True)

# f'select * from User where role = {Roles.STUDENT}
#query ma garni minus

# class Image(models.Model):
#   image = models.ImageField(upload_to=,)
# class Faculty(models.Model):
#   faculty = models.CharField(max_length=5, null=True)



# class Result(models.Model):
#   student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="result")
#   result_semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='result_semester')
#   subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="std_subject")
#   marks = models.FloatField()
class imageModel(models.Model):
  image = models.ImageField(upload_to='images',null=False, blank=False)