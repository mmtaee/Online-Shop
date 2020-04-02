from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import check_password

import re

class UserSignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, label=_("Email"))
    password1 = forms.CharField(max_length=32, widget=forms.PasswordInput, label=_("Password"))
    password2 = forms.CharField(max_length=32, widget=forms.PasswordInput, label=_("Password Confirmation"))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

    def clean_username(self) :
        cleaned_data = super().clean()
        list_ok = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_.@"
        username = self.cleaned_data['username']
        for i in username :
            if i not in list_ok :
                raise ValidationError(_("Invalid username"))
        if User.objects.filter(username=username) :
            raise ValidationError(_("Username is already exist, if your registration is incomplete, continue from login-forgot password"))
        return username

    def clean_email(self):
        cleaned_data = super().clean()
        email = self.cleaned_data['email']
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(email) :
            raise ValidationError(_("Invalid email-type"))
        if User.objects.filter(email=email) :
            raise ValidationError(_("Email is already exist"))
        return email

    def clean_password2(self) :
        cleaned_data = super().clean()
        password2 = self.cleaned_data['password2']
        password1 = self.cleaned_data['password1']
        list_ok = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_."
        for i in password1 :
            if i not in list_ok :
                raise ValidationError(_("Invalid password"))
        if len(password2) < 8 :
                raise ValidationError(_("Minimum length of password must be 8 characters"))
        elif password1 != password2 :
            raise ValidationError(_("Password and confirm password does not match"))
        elif password1.isnumeric() :
            raise ValidationError(_("Password must contain at least one character"))
        return password2

class UserForgotPasswordForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        cleaned_data = super().clean()
        email = self.cleaned_data['email']
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(email) :
            raise ValidationError(_("Invalid email-type"))
        if not User.objects.filter(email=email) :
            raise ValidationError(_("Email not exist"))
        return email

class UserResetPasswordForm(forms.Form):
    new_password = forms.CharField(max_length=32, widget=forms.PasswordInput, label=_("New Passowrd"))

    def clean_new_password(self) :
        cleaned_data = super().clean()
        new_password = self.cleaned_data['new_password']
        list_ok = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_."
        for i in new_password :
            if i not in list_ok :
                raise ValidationError(_("Invalid password"))
        if len(new_password) < 8 :
                raise ValidationError(_("Minimum length of password must be 8 characters"))
        elif new_password.isnumeric() :
            raise ValidationError(_("Password must contain at least one character"))
        return new_password
