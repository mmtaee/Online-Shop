from django.urls import path
from django.views.generic import TemplateView
from .views import (
                ManufacturerListView,
                ManufacturerDetailView,
                ManufacturerCreateView,
                ManufacturerUpdateView,
                ManufacturerDeleteView,

                CategoryListView,
                CategoryCreateView,
                CategoryUpdateView,
                CategoryDeleteView,

)

app_name = "main"

urlpatterns = [
    path('', TemplateView.as_view(template_name="home.html"), name="home"),

    #  Category Urls
    path('category/list/', CategoryListView.as_view(), name='cate_list'),
    path('category/create/', CategoryCreateView.as_view(), name='cate_create'),
    path('category/update/<int:id>/', CategoryUpdateView.as_view(), name='cate_update'),
    path('category/delete/<int:id>/', CategoryDeleteView.as_view(), name='cate_delete'),

    #  Manufacturer Urls
    path('manufacturer/list/',            ManufacturerListView.as_view(),   name='manu_list'),
    path('manufacturer/create/',          ManufacturerCreateView.as_view(), name='manu_create'),
    path('manufacturer/detail/<int:id>/', ManufacturerDetailView.as_view(), name='manu_detail'),
    path('manufacturer/update/<int:id>/', ManufacturerUpdateView.as_view(), name='manu_update'),
    path('manufacturer/delete/<int:id>/', ManufacturerDeleteView.as_view(), name='manu_delete'),


]
