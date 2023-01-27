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

class Faculty(models.Model):
  name = models.CharField(max_length= 10)
class User(models.Model):
  userName = models.CharField(max_length=100, unique=True)
  firstName = models.CharField(max_length=100)
  lastName = models.CharField(max_length=100)
  password = models.CharField(max_length=100)
  role = models.IntegerField()
  address = models.CharField(max_length = 100)
  # image = models.ImageField(upload_to='images',null=False, blank=False)
  image = models.TextField()
  contact_no = models.CharField(max_length=10)
  email = models.EmailField(null=True)
  faculty = models.ForeignKey(Faculty, null=True, on_delete=models.DO_NOTHING)
  batch = models.CharField(max_length=5, null=True)
  semester = models.ForeignKey(Semester, null=True, on_delete=models.DO_NOTHING)

  def __str__(self):
    return f'{self.userName} has role{self.role}'
  
class Transaction(models.Model):
  user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="transaction")
  semester = models.ForeignKey(Semester, null=True, on_delete=models.DO_NOTHING, related_name="semester")
  faculty = models.ForeignKey(Faculty, on_delete=models.DO_NOTHING, related_name = "transaction_semester" )
  type = models.IntegerField(null=True)
  amount = models.FloatField(null=True)
  date = models.DateTimeField(auto_now_add=True)

# f'select * from User where role = {Roles.STUDENT}
#query ma garni minus

class Subject(models.Model):
  faculty = models.ForeignKey(Faculty, on_delete=models.DO_NOTHING, related_name="sub_faculty")
  semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="sem_subject")
  subject = models.CharField(max_length=60)
  full_marks = models.FloatField()
  pass_marks = models.FloatField()

class Marks(models.Model):
  student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student_mark")
  semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='semester_mark')
  subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="subject_mark")
  marks = models.FloatField()

class imageModel(models.Model):
  image = models.TextField()