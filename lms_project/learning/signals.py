from django.db.models.signals import pre_save
from django.dispatch import Signal
from .models import Course, Lesson
from django.db.models import Count


set_views = Signal()


def check_quantity(sender, instance, **kwargs):
    error = None
    course_data = Course.objects.filter(id=instance.course.id).annotate(lessons_count=Count('lessons')).values('count_lessons', 'lessons_count')

    if course_data.lessons_count >= course_data.count_lessons:
        error = f'Количество уроков ограничено!' \
                f'Ранее вы установили, что курс будет содержать {course_data.count_lessons} уроков'
    return error


def incr_views(sender, **kwargs):
    session = kwargs['session']
    views = session.setdefault('views', {})
    course_id = str(kwargs['id'])
    count = views.get(course_id, 0)
    views[course_id] = count + 1
    session['views'] = views
    session.modified = True


pre_save.connect(check_quantity, sender=Lesson)
set_views.connect(incr_views)