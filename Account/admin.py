from django.contrib import admin

from .models import *

admin.site.register(User)
admin.site.register(Semester)
admin.site.register(Transaction)
admin.site.register(imageModel)