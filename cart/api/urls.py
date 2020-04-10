from django.urls import path


from cart.api import views


app_name = "cart_api"

urlpatterns = [
        path('create/', views.CratItemCreateApiView.as_view(), name='cart_create'),
]