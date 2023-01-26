import environ
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import payment as paymentviews
from .views import result_view as resultviews
from .views import user_views as user_views

env = environ.Env()
environ.Env.read_env()

urlpatterns = [
  path('user/create', user_views.userCreate, name="register"),
  path('getInfo/allUser', user_views.getAllInfo, name="Info_all"),
  path('details/<str:username>', user_views.getInfo, name="Info"),
  path('delete/<str:username>', user_views.deleteInfo, name="delete"),
  path('update/<str:username>', user_views.updateInfo, name="update"),
  path('login', user_views.login),
  # path('semester', user_views.semester)
  # # path('hello', views.hello),
  path('transaction/<str:username>', paymentviews.transaction),
  # # path('student/details/<str:username>', views.studentDetails),
  path('due/<str:username>', paymentviews.due),
  # path('khalti', paymentviews.khaltiVerify),
  path('student/payment/details/<str:username>', paymentviews.StudentPaymentDetails),
  path('bulk', paymentviews.bulkBillAdd),
  path('upgrade/semester', paymentviews.upgradeSemester),
  # path('image', user_views.imageUpload),
  # path('image/view', user_views.imageSend),
  # # path('subject', views.subject)
  # path('first_semester/result/<str:username>', resultviews.firstSemesterResult)
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
