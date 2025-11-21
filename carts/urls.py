from django.urls import path

from carts.views import cart_add, cart_change, cart_remove

app_name = 'cart'

urlpatterns = [
    path('cart-add/<slug:product_slug>/', cart_add, name='cart_add'),
    path('cart-change/<int:cart_id>/', cart_change, name='cart_change'),
    path('cart-remove/<int:cart_id>/', cart_remove, name='cart_remove'),
]
