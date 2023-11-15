from django.urls import path
from .views import *


urlpatterns = [
    path('courses/', courses, name='courses'),
    path('courses/<int:course_id>', courses_id, name='courses_id'),
    path('lessons/<int:course_id>', lessons, name='lessons'),
    path('trackings/<int:user_id>', trackings, name='trackings'),
    path('reviews/<int:course_id>', reviews, name='reviews'),
    path('analytics/', analytics, name='analytics'),
    path('users/', users, name='users')
]