from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView

from .models import Manufacturer, Category, Product
from .forms import (
        ManufacturerCreateForm,
        ManufacturerEditForm,
        CategoryModelForm,
)


#  Category Classes
class CategoryObjectMixin(object):
    model = Category

    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None :
            obj = get_object_or_404(self.model, id=id)
        return obj

class CategoryListView(ListView):
    template_name = 'category/list.html'

class CategoryCreateView(View):
    template_name = 'category/create.html'
    def get(self, request, *args, **kwargs):
        form = CategoryModelForm()
        context = {
                'form' : form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = CategoryModelForm(request.POST)
        if form.is_valid():
            new = form.save()
        context = {
                'form' : form,
        }
        return render(request, self.template_name, context)

class CategoryUpdateView(CategoryObjectMixin, View):
    template_name = "category/update.html"

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        form = CategoryModelForm(instance=obj)
        context = {
                    'form' : form,
                    'object' : obj,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        form = CategoryModelForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
        context = {
                    'form' : form,
                    'object' : obj,
        }
        return render(request, self.template_name, context)

class CategoryDeleteView(CategoryObjectMixin, View):
    template_name = "category/delete.html"

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        context = {
                    'object' : obj,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        context = {
                    'object' : obj,
        }
        if obj:
            obj.delete()
        return redirect('main:cate_list')


#  Manufacturer Classes
class ManufacturerObjectMixin(object):
    model = Manufacturer

    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None :
            obj = get_object_or_404(self.model, id=id)
        return obj

class ManufacturerListView(ListView):
    template_name = "manufacturer/list.html"
    queryset = Manufacturer.objects.all()

class ManufacturerDetailView(ManufacturerObjectMixin, DetailView):
    template_name = "manufacturer/detail.html"

class ManufacturerCreateView(View):
    template_name = "manufacturer/create.html"

    def get(self, request, *args, **kwargs):
        form = ManufacturerCreateForm()
        context = {
                'form' : form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = ManufacturerCreateForm(request.POST, request.FILES)
        if form.is_valid():
            new = form.save()
            return redirect('main:manu_detail', id=new.id)
        context = {
                'form' : form,
        }
        return render(request, self.template_name, context)

class ManufacturerUpdateView(ManufacturerObjectMixin,View):
    template_name = "manufacturer/update.html"

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        form = ManufacturerEditForm(instance=obj)
        context = {
                    'form' : form,
                    'object' : obj,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        form = ManufacturerEditForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            new_name = form.cleaned_data.get('new_name', None)
            new = form.save(commit=False)
            if new_name :
                new.name = new_name
            new.save()
            return redirect('main:manu_detail', id=obj.id)
        context = {
                    'form' : form,
                    'object' : obj,
        }
        return render(request, self.template_name, context)

class ManufacturerDeleteView(ManufacturerObjectMixin, View):
    template_name = "manufacturer/delete.html"

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        context = {
                    'object' : obj,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        context = {
                    'object' : obj,
        }
        if obj:
            obj.delete()
        return redirect('main:manu_list')
