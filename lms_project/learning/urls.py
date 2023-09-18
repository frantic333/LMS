from django.urls import path, re_path
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('create/', create, name='create'),
    path('delete/<int:course_id>', delete, name='delete'),
    re_path('^detail/(?P<course_id>[1-9][0-9])/$', detail, name='detail'),
    path('enroll/<int:course_id>', enroll, name='enroll')
]