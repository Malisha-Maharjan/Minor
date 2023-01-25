from django.db import models


class Roles(object):
  ADMIN = 1
  STAFF = 2
  STUDENT = 3

class TransactionsTypes(object):
  BILL = 1
  PAYMENT = 2
  SCHOLARSHIP = 3
class User(models.Model):
  userName = models.CharField(max_length=100, unique=True)
  firstName = models.CharField(max_length=100)
  lastName = models.CharField(max_length=100)
  password = models.CharField(max_length=100)
  role = models.IntegerField()
  email = models.EmailField(null=True)
  faculty = models.CharField(max_length=5, null=True)
  batch = models.CharField(max_length=5, null=True)
  totalFee = models.FloatField(null=True)
  semester = models.IntegerField(null=True)

  def __str__(self):
    return f'{self.userName} has role{self.role}'
  
# # # payment model
class Semester(models.Model):
  student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student")
  std_semester = models.IntegerField()
  is_active = models.BooleanField(default=True)
class Transaction(models.Model):
  transaction = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="transaction")
  type = models.IntegerField(null=True)
  amount = models.FloatField(null=True)
  date = models.DateTimeField(auto_now_add=True)

# f'select * from User where role = {Roles.STUDENT}
#query ma garni minus

# class Image(models.Model):
#   image = models.ImageField(upload_to=,)

class imageModel(models.Model):
  image = models.ImageField(upload_to='images',null=False, blank=False)