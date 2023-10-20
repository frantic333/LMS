from django.db.models.signals import pre_save
from django.dispatch import Signal
from .models import Course, Lesson


set_views = Signal()


def check_quantity(sender, instance, **kwargs):
    error = None
    actual_count = sender.objects.filter(course=instance.course).count()
    set_count = Course.objects.filter(id=instance.course.id).values('count_lessons')[0]['count_lessons']

    if actual_count >= set_count:
        error = f'Количество уроков ограничено!' \
                f'Ранее вы установили, что курс будет содержать {set_count} уроков'
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