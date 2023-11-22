from django.urls import path, include
from .views import *
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('courses/', CourseListAPIView.as_view(), name='courses'),
    path('courses/<int:course_id>', CourseRetrieveAPIView.as_view(), name='courses_id'),
    path('lessons/<int:course_id>', LessonListAPIView.as_view(), name='lessons'),
    path('trackings/<int:user_id>', TrackingListAPIView.as_view(), name='trackings'),
    path('reviews/<int:course_id>', ReviewsListAPIView.as_view(), name='reviews'),
    path('analytics/', analytics, name='analytics'),
    path('users/', users, name='users'),
    # Authrntication urls
    path('authentication/', include('rest_framework.urls')),
    path('generate-token/', obtain_auth_token, name='generate-token'),
    path('users-for-admin/', UserForAdminView.as_view(), name='user-for-admin'),
    path('courses/create/', CourseCreateView.as_view(), name='courses_create'),
    path('courses/delete/<int:course_id>/', CourseDeleteView.as_view(), name='courses_delete')
]