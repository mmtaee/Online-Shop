from django.urls import path
from .views import (
            CartCreateView,

            # checkout,
)

app_name = "cart"

urlpatterns = [
    path('create/', CartCreateView.as_view(), name='create'),
    # path('cart/<int:id>/', views.cart, name='cart_remove'),
    # path('cart_detail/<int:id>/', views.cart_detail, name='cart_detail'),
    # path('cart_history/', views.cart_history, name='cart_history'),

    # path('checkout/', checkout, name='checkout'),
]
