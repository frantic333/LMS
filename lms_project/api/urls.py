from django.urls import path, include
from .views import *
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter(trailing_slash=True)
router.register('analytics', AnalyticViewSet, basename='analytic')
router.register('trackings', TrackingStudentViewSet, basename='tracking')
router.register('trackings_for_authors', TrackingAuthorViewSet, basename='tracking_for_authors')

for url in router.urls:
    print(url)


urlpatterns = [
    path('courses/', CourseListAPIView.as_view(), name='courses'),
    path('courses/<int:course_id>', CourseRetrieveAPIView.as_view(), name='courses_id'),
    path('', include(router.urls)),

    # before using routers
    #path('trackings_for_authors/', TrackingAuthorViewSet.as_view(actions={'get': 'list', 'post': 'create',
    #                                                                      'patch': 'partial_update'}),
    #     name='trackings'),
    #path('trackings_for_authors/<int:course_id>', TrackingAuthorViewSet.as_view(actions={'get': 'retrieve'}),
    #     name='trackings_id'),
    #path('trackings/', TrackingStudentViewSet.as_view(actions={'get': 'list', 'post': 'create'}), name='trackings'),
    #path('trackings/<int:course_id>', TrackingStudentViewSet.as_view(actions={'get': 'retrieve'}), name='trackings_id'),
    #path('analytics/', AnalyticViewSet.as_view(actions={'get': 'list'}), name='analytics'),
    #path('analytics/<int:course_id>', AnalyticViewSet.as_view(actions={'get': 'retrieve'}), name='analytics_id'),

    path('users/', users, name='users'),

    # additionally
    path('reviews/<int:course_id>', ReviewsListAPIView.as_view(), name='reviews'),
    path('lessons/<int:course_id>', LessonListAPIView.as_view(), name='lessons'),

    # Authrntication urls
    path('authentication/', include('rest_framework.urls')),
    path('generate-token/', obtain_auth_token, name='generate-token'),
    path('users-for-admin/', UserForAdminView.as_view(), name='user-for-admin'),
    path('courses/create/', CourseCreateView.as_view(), name='courses_create'),
    path('courses/delete/<int:course_id>/', CourseDeleteView.as_view(), name='courses_delete')
]