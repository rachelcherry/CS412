from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Person)
admin.site.register(Friend)
admin.site.register(Entertainment)
admin.site.register(Recommendation)