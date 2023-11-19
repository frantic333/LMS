from django.urls import path
from .views import *


urlpatterns = [
    path('courses/', CourseListAPIView.as_view(), name='courses'),
    path('courses/<int:course_id>', CourseRetrieveAPIView.as_view(), name='courses_id'),
    path('lessons/<int:course_id>', LessonListAPIView.as_view(), name='lessons'),
    path('trackings/<int:user_id>', trackings, name='trackings'),
    path('reviews/<int:course_id>', reviews, name='reviews'),
    path('analytics/', analytics, name='analytics'),
    path('users/', users, name='users')
]