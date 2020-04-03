from django.urls import path
from .views import (
            CartCreateView,
            CartCheckOutView,
            CartHistoryView,
            CartDetailView,
)

app_name = "cart"

urlpatterns = [
    path('create/', CartCreateView.as_view(), name='create'),
    path('history/', CartHistoryView.as_view(), name='cart_history'),
    path('checkout/', CartCheckOutView.as_view(), name='checkout'),
    path('detail/<int:id>/', CartDetailView.as_view(), name='cart_detail'),


]
