import environ
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views
from .views import *

env = environ.Env()
environ.Env.read_env()

urlpatterns = [
  # path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
  # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  path(env('STUDENT_REGISTER'), views.studentRegister, name="register"),
  path('getInfo', views.getInfo, name="Info"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
