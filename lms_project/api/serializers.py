from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from learning.models import Course, Lesson, Tracking, Review
from auth_app.models import User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

    def to_representation(self, instance):
        return f'{instance.first_name} {instance.last_name}'


class CourseSerializer(ModelSerializer):
    authors = UserSerializer(many=True)

    class Meta:
        model = Course
        fields = '__all__'

    def to_representation(self, instance):
        return f'{instance.title}'


class LessonSerializer(ModelSerializer):
    course = CourseSerializer(many=False)

    class Meta:
        model = Lesson
        fields = '__all__'

    def to_representation(self, instance):
        return f'{instance.name}'


class TrackingSerializer(ModelSerializer):
    lesson = LessonSerializer(many=False)
    user = UserSerializer(many=False)

    class Meta:
        model = Tracking
        fields = '__all__'


class ReviewSerializer(ModelSerializer):
    course = CourseSerializer(many=False)
    user = UserSerializer(many=False)

    class Meta:
        model = Review
        fields = '__all__'
