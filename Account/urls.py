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
  path('register/student', views.studentRegister, name="register"),
  path('getInfo', views.getAllInfo, name="Info_all"),
  path('getInfo/student/<int:id>', views.getInfo, name="Info"),
  path('delete/student/<int:id>', views.deleteInfo, name="delete"),
  path('update/student/<int:id>', views.updateInfo, name="update")
  
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
