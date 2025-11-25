from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    image = models.ImageField(
        upload_to='users_images',
        blank=True,
        null=True,
        verbose_name='Аватар',
    )
    phone_number = models.CharField(max_length=10, blank=True, default='')
    total_orders = models.PositiveIntegerField(verbose_name='Всего заказов', default=0)

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
