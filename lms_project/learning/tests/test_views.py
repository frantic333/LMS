from django.db.models import Q
from django.shortcuts import reverse
from django.test import TestCase, Client
from learning.models import Course, Lesson


class LearningViewTestCase(TestCase):
    fixtures = ['test_data.json']

    def setUp(self) -> None:
        self.client = Client()
        self.index = reverse('index')
        self.create = reverse('create')
        self.tracking = reverse('tracking')

    def test_get_index_view(self):
        response = self.client.get(self.index)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertEqual(len(response.context['courses']), 5)

    def test_get_index_view_by_page(self):
        response = self.client.get(self.index, data={'page': 2})
        self.assertEqual(len(response.context['courses']), 1)

    def test_search_and_order_by_view(self):
        search_query = {'search': 'h', 'price_order': '-price'}
        response = self.client.get(self.index, data=search_query)
        filters = Q(title__icontains=search_query['search']) | Q(description__icontains=search_query['search'])
        courses = Course.objects.filter(filters).order_by(search_query['price_order'])
        self.assertEqual(len(response.context['courses']), len(courses))
        self.assertQuerysetEqual(response.context['courses'], courses)

    def test_get_detail_view(self):
        for course_id in Course.objects.values_list('id', flat=True):
            response = self.client.get(reverse('detail', kwargs={'course_id': course_id}))

            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'detail.html')
            self.assertEqual(len(response.context['lessons']),
                             Lesson.objects.filter(course=course_id).count())

    def test_get_create_view_not_login(self):
        response = self.client.get(path=self.create)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + '?next=' + self.create, status_code=302)

    def test_get_create_view_not_permission_add_course(self):
        login = self.client.login(username='test_student@gmail.com', password='1')
        response = self.client.get(self.create)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'errors/403.html')

    def test_post_create_view(self):
        login = self.client.login(username='test@gmail.com', password='1')
        response = self.client.post(self.create, data={
            'title': 'Python Pro',
            'description': 'Описание 1',
            'start_date': django.utils.timezone.now().date().isoformat(),
            'duration': 3,
            'price': 31000,
            'count_lessons': 15
        })
        course = Course.objects.get(title='Python Pro')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             reverse('create_lesson', kwargs={'course_id': course.id}),
                             status_code=302)

    def test_get_setting_view(self):
        response = self.client.get(reverse('settings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'settings.html')

    def test_post_setting_view(self):
        response = self.client.post(reverse('settings'), data={'paginate_by': 3})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.index, status_code=302)
        self.assertEqual(self.client.cookies.get('paginate_by').value, '3')

        response_index = self.client.get(self.index)
        self.assertEqual(len(response_index.context['courses']), 3)

    def test_get_review_view(self):
        login = self.client.login(username='test_student@gmail.com', password='1')
        course = Course.objects.get(title='HTML')
        response = self.client.get(reverse('review', kwargs={'course_id': course.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review.html')

    def test_post_review_view(self):
        login = self.client.login(username='test_student@gmail.com', password='1')
        course = Course.objects.get(title='HTML')
        response_get = self.client.get(reverse('review', kwargs={'course_id': course.id}))
        response = self.client.post(reverse('review', kwargs={'course_id': course.id}), data={
            'content': 'Курс очень понравился',
            'course': course,
            'user': response_get.context['user']
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('detail', kwargs={'course_id': course.id}), status_code=302)

    def test_add_add_to_favourites(self):
        courses_ids = Course.objects.filter(id__in=[2, 3, 4, 7]).values_list('id', flat=True)
        for course_id in courses_ids:
            response = self.client.post(reverse('add_booking', kwargs={'course_id': course_id}))
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, self.index, status_code=302)
            self.assertIn(course_id, self.client.session.get('favourites'))

    def test_add_remove_favourites(self):
        session = self.client.session
        session['favourites'] = [2, 3, 4, 7]
        session.save()
        response = self.client.post(reverse('remove_booking', kwargs={'course_id': 4}))
        self.assertEqual(len(self.client.session.get('favourites')), 3)
        self.assertRedirects(response, self.index, status_code=302)
        self.assertNotIn(4, self.client.session.get('favourites'))

    def test_get_favourites(self):
        session = self.client.session
        session['favourites'] = [2, 3, 4]
        session.save()
        response = self.client.get(reverse('favourites'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertEqual(len(response.context['courses']), len(session['favourites']))