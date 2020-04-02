from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.contrib.auth import login ,logout, authenticate, REDIRECT_FIELD_NAME
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.auth.forms import AuthenticationForm , PasswordChangeForm # Django Forms for Login and ChangePassword View
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.generic import FormView, RedirectView
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.http import is_safe_url
from django.views import View

import requests
import json

from .forms import(
        UserSignUpForm,
        UserForgotPasswordForm,
        UserResetPasswordForm,
)

from .tocken import account_activation_token
from .models import TokenReset
from .decorators import anonymous_required


class EmailCreator(object):
    def __init__(self):
        self.token = None

    def send_email(self, user):
        current_site = get_current_site(self.request)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        self.token = account_activation_token.make_token(user)
        message = render_to_string (self.render_to_string, {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': uid,
                        'token': self.token,
        })

        email_subject = self.subject
        to_email = user.email
        try :
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()

        except :
            if settings.DEBUG :
                print(message)
            else :
                pass

class UserLoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'login.html'

    @method_decorator(never_cache)
    @method_decorator(csrf_protect)
    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(anonymous_required)
    def dispatch(self, request, *args, **kwargs):
        # Set a cookie >> cookies enabled
        self.request.session.set_test_cookie()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        # test cookie worked >> delete
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
        return super().form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.GET.get('next')
        if not is_safe_url(url=redirect_to, allowed_hosts=self.request.get_host()):
            redirect_to = "/"
        return redirect_to

class UserLogoutView(RedirectView):
    url = "/account/login/"

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)

class UserSignUpView(EmailCreator, FormView):
    form_class = UserSignUpForm
    template_name = 'signup.html'
    subject = "Activation Link"
    render_to_string = "activate_link.html"
    success_url = "/account/login/"
    faild_url = "/account/signup/"

    @method_decorator(anonymous_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        email = self.send_email(user)
        return super().form_valid(form)

class UserActivation(View):

    @method_decorator(anonymous_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        uidb64 = self.kwargs.get('uidb64', None)
        token = self.kwargs.get('token', None)
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=uid)
        if  account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(self.request, user)
            return redirect ('/')
        else:
            raise Http404 ("This link has expired")

class UserForgotPasswordView(EmailCreator, FormView):
    form_class = UserForgotPasswordForm
    template_name = 'forgot_password.html'
    subject = "Password Reset Link"
    render_to_string = "forgot_password_link.html"
    success_url = "/account/login/"
    faild_url = "/account/signup/"

    @method_decorator(anonymous_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        to_email = form.cleaned_data.get('email')
        user = get_object_or_404(User, email=to_email)

        try :
            key = TokenReset.objects.get(user=user)
            key.delete()
        except (TokenReset.DoesNotExist) :
            pass

        email = self.send_email(user)
        key = TokenReset(user=user, resettoken=self.token)
        key.save()
        return super().form_valid(form)

class UserForgotPassword(View):
    template_name = 'reset_passoword.html'

    @method_decorator(anonymous_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        uidb64 = self.kwargs.get('uidb64', None)
        token = self.kwargs.get('token', None)
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=uid)
        if  account_activation_token.check_token(user, token):
            form = UserResetPasswordForm()
            context = {
                    'form':form,
                    'uid':uidb64
            }
            return render(request, self.template_name, context)
        else:
            raise Http404 ("This link has expired")

    def post(self, request, *args, **kwargs):
        form = UserResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            uid = self.kwargs.get('uid', None)
            uid = force_bytes(urlsafe_base64_decode(uid))
            user = get_object_or_404(User, pk=uid)
            user.set_password(new_password)
            user.save()
            print(user.username, new_password)
            _user = authenticate(self.request, username=user.username, password=new_password)
            if _user is not None:
                login(self.request, _user)
                return redirect('/')
            return redirect('user:login')

class UserChangePasswordView(View):
    template_name = "change_password.html"

    @method_decorator(login_required(login_url='/account/login/'))
    def get(self, request, *args, **kwargs):

        form = PasswordChangeForm(request.user)
        context = {
                'form' : form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()

            # Important!
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, request.user)
            # Important!
            
            return redirect("/")
        context = {
                'form' : form,
        }
        return render(request, self.template_name, context)
