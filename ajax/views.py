from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from main.models import *

class GetVaildNameView(View):
    model = None

    @method_decorator(login_required(login_url='/account/login/'))
    def get(self, request, *args, **kwargs):
        if request.is_ajax :
            input = (request.GET.get("input", None)).strip()
            model = (request.GET.get("model", None)).strip()

            if model == "Manufacturer" :
                self.model = Manufacturer
            elif model == "Product" :
                self.model = Product
            elif model == "Category":
                self.model = Category

            if input == "":
                return JsonResponse({}, status = 400)
            if self.model.objects.filter(name__iexact = input).exists():
                return JsonResponse({"valid":False}, status = 200)
            else:
                return JsonResponse({"valid":True}, status = 200)

        return JsonResponse({}, status = 400)

class GetVaildUserNameView(View):
    model = User

    def get(self, request, *args, **kwargs):
        if request.is_ajax :
            input = (request.GET.get("input", None)).strip()
            if input == "":
                return JsonResponse({}, status = 400)
            if self.model.objects.filter(username__iexact = input).exists():
                return JsonResponse({"valid":False}, status = 200)
            else:
                return JsonResponse({"valid":True}, status = 200)

        return JsonResponse({}, status = 400)
