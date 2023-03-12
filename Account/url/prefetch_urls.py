
from django.urls import path

from ..views import prefetch_views as prefetch

urlpatterns = [
  path('faculty', prefetch.getFaculty),
  path('semester', prefetch.getSemesters),
]