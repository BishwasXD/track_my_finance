from django.urls import path
from accounts.views import CreateUserView, UserLoginView, GoogleLoginView

urlpatterns = [
    path('register', CreateUserView.as_view(), name = 'UserRegister'),
    path('login', UserLoginView.as_view(), name = 'Login'),
    path('google-login', GoogleLoginView.as_view(), name='GoogleLogin')
]