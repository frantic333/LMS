from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse('Здесь будет список всех доступных курсов')


def create(request):
    return HttpResponse('Здесь будет форма для создания собственного курса')


def delete(request, course_id):
    return HttpResponse(f'Здесь будет производится удаление {course_id} курса')


def detail(request, course_id):
    return HttpResponse(f'Здесь мы узнаем детальную информацию о {course_id} курсе')


def enroll(request, course_id):
    return HttpResponse(f'Здесь мы сможем записаться на {course_id} курс')