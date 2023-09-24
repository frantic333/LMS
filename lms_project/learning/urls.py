from django.urls import path, re_path
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('create/', create, name='create'),
    path('delete/<int:course_id>', delete, name='delete'),
    path('detail/<int:course_id>', detail, name='detail'),
    path('enroll/<int:course_id>', enroll, name='enroll')
]