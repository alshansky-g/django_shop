from django.urls import path

from users.views import (
    UserLoginView,
    UserRegistrationView,
    logout,
    profile,
    users_cart,
)

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('profile/', profile, name='profile'),
    path('users-cart/', users_cart, name='users_cart'),
    path('logout/', logout, name='logout'),
]
