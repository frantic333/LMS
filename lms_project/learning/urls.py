from django.urls import path, re_path
from .views import *


urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('create/', CourseCreateView.as_view(), name='create'),
    path('update/<int:course_id>/', CourseUpdateView.as_view(), name='update'),
    path('delete/<int:course_id>/', CourseDeleteView.as_view(), name='delete'),
    path('detail/<int:course_id>/', CourseDetailView.as_view(), name='detail'),
    path('enroll/<int:course_id>/', enroll, name='enroll'),
    path('review/<int:course_id>/', review, name='review'),
    path('<int:course_id>/create_lesson/', LessonCreateView.as_view(), name='create_lesson'),
    path('add_booking/<int:course_id>/', add_booking, name='add_booking'),
    path('remove_booking/<int:course_id>/', remove_booking, name='remove_booking'),
    path('favourites/', FavouriteView.as_view(), name='favourites'),
    path('settings/', SettingFormView.as_view(), name='settings')
]