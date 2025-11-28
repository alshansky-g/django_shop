from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from carts.models import Cart
from common.mixins import CacheMixin
from orders.models import Order
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.get_user()
        auth.login(self.request, user)
        Cart.objects.filter(session_key=session_key).update(user=user)
        messages.success(self.request, f'Добро пожаловать, {user.first_name or user.username}.')
        return super().form_valid(form)

    def get_success_url(self):
        if redirect_page := self.request.POST.get('next'):
            return redirect_page
        return reverse_lazy('main:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Home - Авторизация'})
        return context


class UserRegistrationView(CreateView):
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url: str = reverse_lazy('user:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Home - Регистрация'})
        return context

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.save()
        auth.login(self.request, user)
        Cart.objects.filter(session_key=session_key).update(user=user)
        messages.success(
            self.request,
            f'{user.first_name or user.username}, вы успешно зарегистрировались и вошли в аккаунт.',
        )
        return HttpResponseRedirect(self.success_url)


class UserProfileView(LoginRequiredMixin, CacheMixin, UpdateView):
    template_name = 'users/profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('user:profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Профиль успешно обновлен')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Профиль'

        orders = (
            Order.objects.filter(user=self.request.user)
            .prefetch_related('orderitem_set__product')
            .order_by('-id')
        )

        context['orders'] = self.set_get_cache(orders, f'user_{self.request.user.pk}_orders', 60)
        return context


class UserCartView(TemplateView):
    template_name = 'users/users_cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Корзина'
        return context


@login_required
def logout(request):
    messages.success(
        request, f'{request.user.first_name or request.user.username}, вы вышли из аккаунта.'
    )
    auth.logout(request)
    return redirect(reverse('main:index'))
