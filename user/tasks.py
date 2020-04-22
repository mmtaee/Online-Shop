# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task

from django.utils.decorators import method_decorator
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User

from .tocken import account_activation_token


@shared_task
def send_email_task(user_pk, domain, template, subject):
    user = User.objects.get(pk=user_pk)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    message = render_to_string (template, {
                    'user': user,
                    'domain': domain,
                    'uid': uid,
                    'token': token,
    })
    email_subject = subject
    to_email = user.email
    try :
        email = EmailMessage(email_subject, message, to=[to_email])
        email.send()
    except :
        return False

    return True
