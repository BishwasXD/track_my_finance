from django.urls import path
from accounts.views import CreateUserView, UserLoginView

urlpatterns = [
    path('register', CreateUserView.as_view(), name = 'UserRegister'),
    path('login', UserLoginView.as_view(), name = 'Login')
]