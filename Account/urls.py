import environ
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import payment as paymentviews
from .views import views as views

env = environ.Env()
environ.Env.read_env()

urlpatterns = [
  path('user/create', views.userCreate, name="register"),
  path('getInfo/allUser', views.getAllInfo, name="Info_all"),
  path('details/<str:username>', views.getInfo, name="Info"),
  path('delete/<str:username>', views.deleteInfo, name="delete"),
  path('update/<str:username>', views.updateInfo, name="update"),
  path('login', views.login),
  # path('hello', views.hello),
  path('transaction/<str:username>', paymentviews.transaction),
  # path('student/details/<str:username>', views.studentDetails),
  path('due/<str:username>', paymentviews.due),
  path('khalti', paymentviews.khaltiVerify),
  path('student/payment/details/<str:username>', paymentviews.StudentPaymentDetails),
  path('bulk', paymentviews.bulkBillAdd),
  path('upgrade/semester', paymentviews.upgradeSemester),
  path('image', views.imageUpload),
  path('image/view', views.imageSend)
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
