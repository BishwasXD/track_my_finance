from django.urls import path
from accounts.views import CreateUserView, UserLoginView, GoogleLoginView, VerifyTokenView

urlpatterns = [
    path('register', CreateUserView.as_view(), name = 'UserRegister'),
    path('login', UserLoginView.as_view(), name = 'Login'),
    path('verify-token',VerifyTokenView.as_view(),name='verify-token'),
    path('google-login', GoogleLoginView.as_view(), name='GoogleLogin')
]