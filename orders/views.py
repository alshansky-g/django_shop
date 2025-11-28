from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.forms import ValidationError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from orders.forms import CreateOrderForm
from orders.services import transaction_processed


class CreateOrderView(LoginRequiredMixin, FormView):
    template_name = 'orders/create_order.html'
    form_class = CreateOrderForm
    success_url = reverse_lazy('user:profile')

    def get_initial(self):
        initial = super().get_initial()
        initial['first_name'] = getattr(self.request.user, 'first_name', '')
        initial['last_name'] = getattr(self.request.user, 'last_name', '')
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Оформление заказа'
        context['order'] = True
        return context

    def form_valid(self, form):
        try:
            with transaction.atomic():
                if transaction_processed(self.request, form):
                    return redirect('user:profile')

        except ValidationError as e:
            messages.error(self.request, str(e))
            return redirect('cart:order')
