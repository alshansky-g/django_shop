from decimal import Decimal

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    class Meta:
        db_table = 'categories'
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(
        upload_to='goods_images', blank=True, null=True, verbose_name='Изображение'
    )
    price = models.DecimalField(
        default=Decimal(0.00), max_digits=7, decimal_places=2, verbose_name='Цена'
    )
    discount = models.DecimalField(
        default=Decimal(0.00), max_digits=4, decimal_places=2, verbose_name='Скидка в %'
    )
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, verbose_name='Категория')

    class Meta:
        db_table = 'products'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self) -> str:
        return self.name

    def show_id(self):
        return f'{self.id:05}'

    def price_with_discount(self):
        return round(self.price * (1 - self.discount / 100), 2)
