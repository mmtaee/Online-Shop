from django.contrib import admin

from .models import Manufacturer, Category, Product

admin.site.register(Manufacturer)
admin.site.register(Category)
admin.site.register(Product)
