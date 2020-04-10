from django.urls import path
from main.api import views

from main.api import views


app_name = "main_api"

urlpatterns = [
        path('manaufacture_list/', views.ManufacturerListApiView.as_view(), name='manaufacture_list'),
        path('manaufacture_detail/<int:id>/', views.ManufacturerDetailApiView.as_view(), name='manaufacture_detail'),

        path('category_list/', views.CategoryListApiView.as_view(), name='category_list'),
        path('category_detail/<int:id>/', views.CategoryDetailApiView.as_view(), name='category_detail'),

        path('product_list/', views.ProductListApiView.as_view(), name='product_list'),
        path('product_detail/<int:id>/', views.ProductDetailApiView.as_view(), name='product_detail'),
        
        path('productbymanufacturer_list/<int:id>/', views.ProductListByManufacturerApiView.as_view(), name='productbymanufacturer_list'),
        path('productbycategory_list/<int:id>/', views.ProductListByCategoryApiView.as_view(), name='productbycategory_list'),
        path('productbytag_list/<str:name>/', views.ProductListByTagNameApiView.as_view(), name='productbytag_list'),

        path('tag_list/', views.TagsListApiView.as_view(), name='tag_list'),

]


