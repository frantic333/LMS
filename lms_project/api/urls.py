from django.urls import path, include
from .views import *
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token



from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="заголовок",
      default_version='v1',
      description="Описание",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)





router = DefaultRouter(trailing_slash=True)
router.register('analytics', AnalyticViewSet, basename='analytic')
router.register('trackings', TrackingStudentViewSet, basename='tracking')
router.register('trackings_for_authors', TrackingAuthorViewSet, basename='tracking_for_authors')

for url in router.urls:
    print(url)


urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
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