from django.urls import path

from ..views import user_views as user_views

urlpatterns = [
  path('user/create', user_views.userCreate, name="register"),
  path('getInfo/allUser', user_views.getAllInfo, name="Info_all"),
  path('student/details', user_views.getStudent),
  path('details/<str:username>', user_views.getInfo, name="Info"),
  path('delete/<str:username>', user_views.deleteInfo, name="delete"),
  path('user/update/<str:username>', user_views.updateInfo, name="update"),
  path('password/update/<str:username>', user_views.updatePassword),
  path('forgot/password', user_views.forgotPassword),
  path('login', user_views.login),
  path('upgrade/semester', user_views.upgradeSemester),
  # path('update/<int:id>', user_views.updateSemester)
]