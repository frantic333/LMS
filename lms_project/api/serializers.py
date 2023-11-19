from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer, ValidationError
from django.utils.timezone import datetime
from django.db.models import Count, Sum
from learning.models import Course, Lesson, Tracking, Review
from auth_app.models import User


class UserRepresentationSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

    def to_representation(self, instance):
        return f'{instance.first_name} {instance.last_name}'


class CourseRepresentationSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

    def to_representation(self, instance):
        return f'{instance.title}'


class LessonRepresentationSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

    def to_representation(self, instance):
        return f'{instance.name}'


class CourseSerializer(ModelSerializer):
    authors = UserRepresentationSerializer(many=True)

    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(ModelSerializer):
    course = CourseRepresentationSerializer(many=False)

    class Meta:
        model = Lesson
        fields = '__all__'


class TrackingSerializer(ModelSerializer):
    lesson = LessonRepresentationSerializer(many=False)
    user = UserRepresentationSerializer(many=False)

    class Meta:
        model = Tracking
        fields = '__all__'


class ReviewSerializer(ModelSerializer):
    course = CourseRepresentationSerializer(many=False)
    user = UserRepresentationSerializer(many=False)

    class Meta:
        model = Review
        fields = '__all__'


class AnalyticCourseSerializer(Serializer):
    course = serializers.SerializerMethodField()
    views = serializers.SerializerMethodField()
    count_students = serializers.SerializerMethodField()
    percent_passed = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    def get_course(self, instance) -> str:
        return instance.course.title

    def get_views(self, instance) -> int:
        request = self.context.get('request')
        views_dict = request.session.get('views', {})
        return views_dict.get(str(instance.course.id), 0)

    def get_url(self, instance) -> str:
        request = self.context.get('request')
        return f'{request.scheme}://{request.META["HTTP_HOST"]}{instance.course.get_absolute_url()}'

    def get_count_students(self, instance) -> int:
        total_students = Tracking.objects\
            .filter(lesson__course=instance.course.id)\
            .values('lesson__course')\
            .aggregate(Count('user', distinct=True))
        return total_students['user__count']

    def get_percent_passed(self, instance) -> float:
        course_id = instance.course.id
        students = Tracking.objects.filter(lesson__course=course_id).values('user').distinct()
        users_percent = list()
        for id in range(len(students)):
            percents = Tracking.objects.filter(lesson__course=course_id, user=students[id]['user']).\
                aggregate(total=Count('lesson'), fact=Sum('passed'))
            user_percent = float(percents['fact'] / percents['total'] * 100)
            users_percent.append(user_percent)
        try:
            total_percent = round(sum(users_percent) / len(users_percent), 2)
            return total_percent
        except ZeroDivisionError:
            return 0


class AnalyticSerializer(Serializer):
    report_date = serializers.SerializerMethodField()
    data = serializers.SerializerMethodField()

    def get_report_date(self, instance):
        return datetime.now()

    def get_data(self, instance):
        return AnalyticCourseSerializer(instance=instance, many=True, context=self.context).data


class UserSerializer(ModelSerializer):
    first_name = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(write_only=True, required=True)
    description = serializers.CharField(max_length=200, default='', required=False, allow_null=True)
    avatar = serializers.ImageField(use_url=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'password', 'email',
                  'birthday', 'description', 'avatar')
        extra_kwargs = {
            'password': {
               'write_only': True,
            }
        }

    def to_internal_value(self, data):
        data['first_name'] = ''
        data['last_name'] = ''
        return data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['name'] = instance.get_full_name()
        return data

    def validate(self, data):
        errors = []
        name = data.get('name').split()
        if not name or len(name) == 1:
            errors.append({'name': 'Не указано имя и фамилия для нового пользователя'})
        if len(data.get('description')) > 200:
            errors.append({'description': 'Описание слишком большое (max = 200 символов)'})
        if errors:
            raise ValidationError({'errors': errors})
        return data

    def save(self, validated_data):

        #convert all values to string (to add ava)
        *converted_dict, = map(lambda x: dict(zip(dict(validated_data).keys(), x)),
                              zip(*dict(validated_data).values()))
        validated_data = dict(*converted_dict)
        print(validated_data)

        name = validated_data.pop('name').split()
        validated_data['first_name'] = name[0]
        validated_data['last_name'] = name[1]
        user = User(**validated_data)
        user.set_password(validated_data['password'][0])
        user.save()
        return user