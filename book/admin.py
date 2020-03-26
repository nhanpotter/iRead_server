from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(Comment)
admin.site.register(Rating)