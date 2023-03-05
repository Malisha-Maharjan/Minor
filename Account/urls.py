import environ
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import payment_views as payment_views
from .views import prefetch_views as prefetch
from .views import result_view as result_views
from .views import subject_views as subject_views
from .views import user_views as user_views

env = environ.Env()
environ.Env.read_env()

urlpatterns = [
  path('faculty', prefetch.getFaculty),
  path('semester', prefetch.getSemesters),
  path('user/create', user_views.userCreate, name="register"),
  path('getInfo/allUser', user_views.getAllInfo, name="Info_all"),
  path('student/details', user_views.getStudent),
  path('details/<str:username>', user_views.getInfo, name="Info"),
  path('delete/<str:username>', user_views.deleteInfo, name="delete"),
  path('user/update/<str:username>', user_views.updateInfo, name="update"),
  path('password/update/<str:username>', user_views.updatePassword),
  path('forgot/password', user_views.forgotPassword),
  path('login', user_views.login),
  path('subject', subject_views.addSubject),
  path('subject/<int:faculty>/<int:semester>', subject_views.getSubject),
  path('subject/<int:faculty>/<int:semester>/<str:subject>', subject_views.deleteSubject),
  path('add/mark/<str:username>/<int:semester>', result_views.addMark),
  path('mark/<str:username>/<int:id>', result_views.getMark),
  path('mark/update/<str:username>/<int:semester>', result_views.updateMarks),

  # path('subject/<str:name>', subject_views.getSubject),
  # path('semester', user_views.semester)
  path('transaction', payment_views.transaction),
  # # path('student/details/<str:username>', views.studentDetails),
  path('due/<str:username>', payment_views.due),
  path('khalti', payment_views.khaltiVerify),
  path('payment/details/<str:username>', payment_views.StudentPaymentDetails),
  path('bulk', payment_views.bulkBillAdd),
  path('upgrade/semester', payment_views.upgradeSemester),
  path('mark', prefetch.mark),
  path('graph/data/<str:username>', result_views.getGraph)
  # # path('subject', views.subject)
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
