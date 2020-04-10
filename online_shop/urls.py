from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('main/', include('main.urls')),
    path('main/api/', include('main.api.urls'),),

    path('cart/', include('cart.urls')),
    path('cart/api/', include('cart.api.urls'),),

    path('account/', include('user.urls')),
    path('account/api/', include('user.api.urls'),),
    
    path('ajax/', include('ajax.urls')),
    path('', TemplateView.as_view(template_name="home.html"), name="home"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
