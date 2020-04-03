from django.urls import path
from .views import (
                TaggedView,

                ManufacturerListView,
                ManufacturerDetailView,
                ManufacturerCreateView,
                ManufacturerUpdateView,
                ManufacturerDeleteView,

                CategoryListView,
                CategoryCreateView,
                CategoryUpdateView,
                CategoryDeleteView,

                ProductListView,
                ProductDetailView,
                ProductCreateView,
                ProductUpdateView,
                ProductDeleteView,
)

app_name = "main"

urlpatterns = [
    # Tagged urls
    path('tag/<slug:slug>/', TaggedView.as_view(), name="tagged"),

    #  Product Urls
    path('product/list/',              ProductListView.as_view(),   name='product_list'),
    path('product/create/',            ProductCreateView.as_view(), name='product_create'),
    path('product/detail/<int:id>/',   ProductDetailView.as_view(), name='product_detail'),
    path('product/update/<int:id>/',   ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:id>/',   ProductDeleteView.as_view(), name='product_delete'),


    #  Category Urls
    path('category/list/',            CategoryListView.as_view(),   name='category_list'),
    path('category/create/',          CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:id>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:id>/', CategoryDeleteView.as_view(), name='category_delete'),

    #  Manufacturer Urls
    path('manufacturer/list/',            ManufacturerListView.as_view(),   name='manufacturer_list'),
    path('manufacturer/create/',          ManufacturerCreateView.as_view(), name='manufacturer_create'),
    path('manufacturer/detail/<int:id>/', ManufacturerDetailView.as_view(), name='manufacturer_detail'),
    path('manufacturer/update/<int:id>/', ManufacturerUpdateView.as_view(), name='manufacturer_update'),
    path('manufacturer/delete/<int:id>/', ManufacturerDeleteView.as_view(), name='manufacturer_delete'),
]
