from django.db import models
from django.contrib.auth.models import AbstractUser
from .functions import get_timestamp_path_user


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email')
    username = models.CharField(verbose_name='Username', max_length=10, unique=False)
    birthday = models.DateField(verbose_name='Дата рождения', null=True)
    description = models.TextField(verbose_name='Обо мне', null=True, default='', max_length=150)
    avatar = models.ImageField(verbose_name='Фото', blank=True, upload_to=get_timestamp_path_user)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name_plural = 'Участники'
        verbose_name = 'Участник'
        ordering = ['last_name']

    def __str__(self):
        return f'Участник {self.first_name} {self.last_name}: {self.email}'

    def natural_key(self):
        # first_name, last_name
        return self.get_full_name()