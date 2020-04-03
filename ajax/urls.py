from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from ajax.views import (
                GetVaildNameView,
                GetVaildUserNameView,
)

urlpatterns = [
        path('check_name/', GetVaildNameView.as_view()),
        path('check_username/', GetVaildUserNameView.as_view()),
]
