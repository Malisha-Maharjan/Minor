from django.conf.urls.static import static
from django.urls import path

from ..views import result_view as result_views

urlpatterns = [
  path('add/mark/<str:username>/<int:semester>', result_views.addMark),
  path('mark/<str:username>/<int:id>', result_views.getMark),
  path('mark/update/<str:username>/<int:semester>', result_views.updateMarks),
  path('graph/data/<str:username>', result_views.getGraph),
  path('prediction/<str:username>', result_views.model)
]
