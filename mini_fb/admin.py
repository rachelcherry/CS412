#Rachel Cherry
#rcherry@bu.edu
from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Profile)
admin.site.register(StatusMessage)