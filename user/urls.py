from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from user.views import (
            UserLoginView,
            UserLogoutView,
            UserSignUpView,
            UserActivation,
            UserForgotPasswordView,
            UserForgotPassword,
            UserChangePasswordView,
)

app_name = 'user'

urlpatterns = [
    path('login/',  UserLoginView.as_view(),  name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('signup/', UserSignUpView.as_view(), name='signup'),
    path('forgot_password/', UserForgotPasswordView.as_view(), name='forgot_password'),
    path('change_password/', UserChangePasswordView.as_view(), name='change_password'),
    path('reset_password/uid=<str:uid>', UserForgotPassword.as_view(), name='reset_password'),
    path('activate/uid=<str:uidb64>/token=<str:token>',UserActivation.as_view(), name='activate'),
    path('forgot_password_check/uid=<str:uidb64>/token=<str:token>', UserForgotPassword.as_view(), name='forgot_password_check'),
]
