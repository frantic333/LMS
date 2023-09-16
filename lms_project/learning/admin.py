from django.contrib import admin
from .models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'start_date', 'description')
#    exclude = ('description', 'duration', 'price')
    search_fields = ('title', 'start_date', 'description')
    list_per_page = 3
    actions_on_top = True
    actions_selection_counter = True
    list_display_links = ('title',)
    list_editable = ('description',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('course', 'name', 'preview')
    search_fields = ('name',)
    list_per_page = 5
    actions_on_top = True
    actions_selection_counter = True
