from django.contrib import messages
from django.forms import ValidationError

from carts.models import Cart
from orders.models import Order, OrderItem


def transaction_processed(request, form):
    user = request.user
    user.total_orders += 1
    user.save()
    cart_items = Cart.objects.filter(user=user)

    if cart_items.exists():
        order = Order.objects.create(
            user=user,
            phone_number=form.cleaned_data['phone_number'],
            requires_delivery=form.cleaned_data['requires_delivery'],
            delivery_address=form.cleaned_data['delivery_address'],
            payment_upon_delivery=form.cleaned_data['payment_upon_delivery'],
            user_order_no=user.total_orders,
        )
        for cart_item in cart_items:
            product = cart_item.product
            name = cart_item.product.name
            price = cart_item.product.actual_price()
            quantity = cart_item.quantity

            if product.quantity < quantity:
                msg = f'Недостаточно товара {name} на складе. В наличии {product.quantity}'
                raise ValidationError(msg)
            OrderItem.objects.create(
                order=order,
                product=product,
                name=name,
                price=price,
                quantity=quantity,
            )
            product.quantity -= quantity
            product.save()
        cart_items.delete()
        messages.success(request, 'Заказ оформлен!')
        return True
    return False
