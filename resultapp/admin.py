from django.contrib import admin
from .models import *
from .views import *

admin.site.register(Branch)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Notice)
admin.site.register(Result)

# Register your models here.
