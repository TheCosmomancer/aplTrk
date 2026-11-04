from django.contrib import admin

from .models import *

# Register your models here.

########## Global Objects ##########
admin.site.register(University)
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Professor)

########## Personal Objects ##########
admin.site.register(User)
admin.site.register(Mail)
admin.site.register(Application)
admin.site.register(Document)