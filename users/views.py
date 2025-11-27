from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from carts.models import Cart
from orders.models import Order, OrderItem
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


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлен.')
            return HttpResponseRedirect(reverse('user:profile'))
    else:
        form = UserProfileForm(instance=request.user)

    orders = (
        Order.objects.filter(user=request.user)
        .prefetch_related(
            Prefetch('orderitem_set', queryset=OrderItem.objects.select_related('product'))
        )
        .order_by('-id')
    )
    context = {'title': 'Home - Профиль', 'form': form, 'orders': orders}
    return render(request, 'users/profile.html', context)


@login_required
def logout(request):
    messages.success(
        request, f'{request.user.first_name or request.user.username}, вы вышли из аккаунта.'
    )
    auth.logout(request)
    return redirect(reverse('main:index'))


def users_cart(request):
    return render(request, 'users/users_cart.html')
