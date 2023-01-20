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
  # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  path('user/create', views.userCreate, name="register"),
  path('getInfo', views.getAllInfo, name="Info_all"),
  path('getInfo/student/<int:id>', views.getInfo, name="Info"),
  path('delete/student/<int:id>', views.deleteInfo, name="delete"),
  path('update/student/<int:id>', views.updateInfo, name="update"),
  path('login', views.login),
  path('hello', views.hello),
  path('student/<int:id>', views.student),
  path('manualPayment/<str:username>', paymentviews.manualPayment),
  path('details/<str:username>', views.details),
  path('due/<str:username>', paymentviews.due),
  path('khalti', paymentviews.khaltiVerify)
  
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
