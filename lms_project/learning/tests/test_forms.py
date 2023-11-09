from django.forms.utils import ValidationError
from django.test import TestCase
from learning.forms import LessonForm
from learning.models import Course


class LearningFormTestCase(TestCase):
    fixtures = ['test_data.json']

    def setUp(self) -> None:
        self.data = {
            'course': Course.objects.get(title='test').id,
            'name': 'test01',
            'preview': 'Страница лендинга или Landing Page - самая ключевая страница, ' 
            'поэтому должна содержать в себе краткую, но важную информацию.'
            'Страница лендинга или Landing Page - самая ключевая страница, ' 
            'поэтому должна содержать в себе краткую, но важную информацию, '
            'предложение для посетителя сайта.'
        }

    def test_lesson_form_preview_length_error(self):
        form = LessonForm(data=self.data)
        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(ValidationError, 'Слишком длинное описание! Сократите до 200 символов')