from django.db import models

from goods.models import Product
from users.models import User


class OrderItemQueryset(models.QuerySet):
    def total_price(self) -> int:
        return sum(item.products_price for item in self)

    def total_quantity(self) -> int:
        if self:
            return sum(item.quantity for item in self)
        return 0


class Order(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.SET_DEFAULT,
        verbose_name='Пользователь',
        blank=True,
        null=True,
        default=None,
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона')
    requires_delivery = models.BooleanField(default=False, verbose_name='Доставка')
    delivery_address = models.TextField(blank=True, default='', verbose_name='Адрес доставки')
    payment_upon_delivery = models.BooleanField(default=False, verbose_name='Оплата при получении')
    is_paid = models.BooleanField(default=False, verbose_name='Оплачено')
    status = models.CharField(max_length=50, default='В обработке', verbose_name='Статус заказа')

    class Meta:
        db_table = 'orders'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self) -> str:
        if self.user:
            return f'Заказ № {self.pk} Покупатель {self.user.first_name} {self.user.last_name}'
        return f'Заказ № {self.pk} Покупатель неизвестен'


class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(
        to=Product, on_delete=models.SET_DEFAULT, null=True, verbose_name='Товар', default=None
    )
    name = models.CharField(max_length=150, verbose_name='Название')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата продажи')

    objects = OrderItemQueryset.as_manager()

    class Meta:
        db_table = 'order_items'
        verbose_name = 'Проданный товар'
        verbose_name_plural = 'Проданные товары'

    def __str__(self) -> str:
        return f'Товар {self.name} Заказ № {self.order.pk}'

    def products_price(self):
        return round(self.price * self.quantity, 2)
