from django.contrib import admin
from .models import User
from django.contrib.auth.models import Group


admin.site.site_header='Learning Management System'
admin.site.register(User)