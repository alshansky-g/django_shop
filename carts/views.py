from django.http import HttpRequest, JsonResponse
from django.views import View

from carts.mixins import CartMixin
from carts.models import Cart
from goods.models import Product


class CartAddView(CartMixin, View):
    def post(self, request: HttpRequest):
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)

        cart = self.get_cart(request, product=product)

        if cart:
            cart.quantity += 1
            cart.save()
        else:
            user = request.user if request.user.is_authenticated else None
            session_key = request.session.session_key if not request.user.is_authenticated else ''
            Cart.objects.create(
                user=user,
                session_key=session_key,
                product=product,
                quantity=1,
            )
        response_data = {
            'message': 'Товар добавлен в корзину',
            'cart_items_html': self.render_cart(request),
        }
        return JsonResponse(response_data)


class CartChangeView(CartMixin, View):
    def post(self, request: HttpRequest):
        cart_id = request.POST.get('cart_id')
        quantity = request.POST.get('quantity')
        cart = self.get_cart(request, cart_id=cart_id)

        if cart and quantity:
            cart.quantity = int(quantity)
            cart.save()
            quantity = cart.quantity

        response_data = {
            'message': 'Количество изменено',
            'quantity': quantity,
            'cart_items_html': self.render_cart(request),
        }
        return JsonResponse(response_data)


class CartRemoveView(CartMixin, View):
    def post(self, request: HttpRequest):
        cart_id = request.POST.get('cart_id')
        cart = self.get_cart(request, cart_id=cart_id)
        if cart:
            quantity = cart.quantity
            cart.delete()

        response_data = {
            'message': 'Товар удален из корзины',
            'cart_items_html': self.render_cart(request),
            'quantity_deleted': quantity,
        }
        return JsonResponse(response_data)
