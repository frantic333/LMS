from django.urls import path
from .views import *


urlpatterns = [
    path('login/', log_in, name='login'),
    path('register/', register, name='register'),
    path('logout/', log_out, name='logout'),
    path('change-password/', change_password, name='change_password'),
    path('reset-password/', reset_password, name='reset_passord')
]