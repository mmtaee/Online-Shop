from django.urls import path


from cart.api import views


app_name = "cart_api"

urlpatterns = [
        path('create/', views.CratItemCreateApiView.as_view(), name='cart_create'),
        path('cartitem_list/', views.CratItemListApiView.as_view(), name='cartitem_list'),
        path('checkout/', views.CartCheckOutApiView.as_view(), name='cart_checkout'),
        path('list/', views.CartListApiView.as_view(), name='cart_list'),
        path('detail/<int:id>/', views.CartDetailApiView.as_view(), name='cart_detail'),
]
