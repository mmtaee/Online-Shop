from rest_framework import serializers

from django.contrib.auth.models import User

import re

def password_validator(view_function):

    def wrapp(request, password ,*args, **kwargs):
        list_ok = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_."
        for i in password :
            if i not in list_ok :
                error = "Invalid password"
                raise serializers.ValidationError(error)
        if len(password) < 8 :
            error = "Minimum length of password must be 8 characters"
            raise serializers.ValidationError(error)
        elif password.isnumeric() :
            error = "Password must contain at least one character"
            raise serializers.ValidationError(error)
        return view_function(request, password ,*args, **kwargs)

    return wrapp


def email_validator(view_function):

    def wrap(request, email ,*args, **kwargs):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(email) :
            error = "Invalid email-type"
            raise serializers.ValidationError(error)
        if User.objects.filter(email=email) :
            error = "Email is already exist"
            raise serializers.ValidationError(error)
        return view_function(request, email ,*args, **kwargs)

    return wrap
