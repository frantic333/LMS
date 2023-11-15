from django.db.models import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from django.db import IntegrityError
from rest_framework import status
from .analytics import AnalyticReport
from learning.models import Course, Lesson, Tracking, Review
from auth_app.models import User
from .serializers import (CourseSerializer, LessonSerializer, TrackingSerializer, ReviewSerializer,
                          AnalyticCourseSerializer, AnalyticSerializer, UserSerializer)


@api_view(['GET', 'POST'])
def courses(request):
    courses = Course.objects.all()
    courses_serializers = CourseSerializer(instance=courses, many=True)
    return Response(data=courses_serializers.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def courses_id(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
        course_serializer = CourseSerializer(instance=course, many=False)
        return Response(data=course_serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as exception:
        return Response(data={'error': 'Запрашиваемый курс отсутствует в системе'},
                        status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def lessons(request, course_id):
    try:
        lesson = Lesson.objects.filter(course=course_id)
        lesson_serializer = LessonSerializer(instance=lesson, many=True)
        return Response(data=lesson_serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as exception:
        return Response(data={'error': 'Запрашиваемый курс отсутствует в системе'},
                        status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def trackings(request, user_id):
    try:
        tracking = Tracking.objects.filter(user=user_id)
        tracking_serializer = TrackingSerializer(instance=tracking, many=True)
        return Response(data=tracking_serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as exception:
        return Response(data={'error': 'Запрашиваемый пользователь не зарегистрирован на сайте'},
                        status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def reviews(request, course_id):
    try:
        review = Review.objects.filter(course=course_id)
        review_serializer = ReviewSerializer(instance=review, many=True)
        return Response(data=review_serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as exception:
        return Response(data={'error': 'Запрашиваемый курс отсутствует в системе'},
                        status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def analytics(request):
    courses = Course.objects.all()
    reports = [AnalyticReport(course=course) for course in courses]
    analytic_serializer = AnalyticSerializer(reports, many=False, context={'request': request})
    return Response(data=analytic_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def users(request):
    if request.method == 'GET':
        users = User.objects.all()
        user_serializer = UserSerializer(instance=users, many=True,)
        return Response(data=user_serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        user_serializer = UserSerializer(data=request.data)
        try:
            if user_serializer.is_valid(raise_exception=True):
                user_serializer.instance = user_serializer.save(user_serializer.validated_data)
                return Response(data=user_serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError:
            return Response(data=user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response(data={'email': 'Пользователь с таким email уже существует'},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as exception:
            return Response(data={'error': str(exception)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)