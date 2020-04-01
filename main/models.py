from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager

import os

def image_renamer(instance, filename):
    class_name = instance.__class__.__name__
    if class_name == "MultipleImages" :
        return os.path.join(str(class_name), str(instance.product), filename)
    return os.path.join(str(class_name), filename)

class Manufacturer(models.Model):
    name    = models.CharField(max_length=200)
    image   = models.ImageField(upload_to=image_renamer)
    desc    = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('main:manufacturer_detail', kwargs={'id':self.id})


class Category(models.Model):
    name    = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('main:category_detail', kwargs={'id':self.id})


class Product(models.Model):
    manufacturer    = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, null=True, blank=True)
    category        = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    name            = models.CharField(max_length=200)
    model           = models.CharField(max_length=200, null=True)
    image           = models.ImageField(upload_to=image_renamer)
    slug            = models.SlugField(unique=True, max_length=100)
    desc            = models.TextField(null=True, blank=True)
    off             = models.IntegerField(null=True)
    create          = models.DateTimeField(auto_now=False, auto_now_add=True)
    update          = models.DateTimeField(auto_now=True, auto_now_add=False)
    stock           = models.IntegerField(null=True, blank=True)
    initial_price   = models.CharField(max_length=300)
    final_price     = models.CharField(max_length=300)
    tags = TaggableManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.off == None:
            self.off = 0
        if self.stock == None:
            self.stock = 0
        initial_price = int(self.initial_price.replace(",", ""))
        final_price = int(initial_price * (1 - (self.off/100)))
        self.final_price = '{0:,}'.format(final_price)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('main:product_detail', kwargs={'id':self.id})


class MultipleImages(models.Model):
    product  = models.ForeignKey(Product, on_delete=models.CASCADE,)
    image    = models.ImageField(upload_to=image_renamer, null=True)

    def __str__(self):
        return self.image.name
