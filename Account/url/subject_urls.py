
from django.urls import path

from ..views import subject_views as subject_views

urlpatterns = [
  path('subject', subject_views.addSubject),
  path('subject/<int:faculty>/<int:semester>', subject_views.getSubject),
  path('subject/<int:faculty>/<int:semester>/<str:subject>', subject_views.deleteSubject)
]