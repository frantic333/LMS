from django.urls import path
from .views import *


urlpatterns = [
    path('login/', login),
    path('register/', register),
    path('logout/', logout),
    path('change-password/', change_password),
    path('reset-password/', reset_password)
]