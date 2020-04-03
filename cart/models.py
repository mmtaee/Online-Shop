from django.db import models
from django.contrib.auth.models import User

from datetime import datetime
from main.models import Product

class Cart(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(default=datetime.now)
    checkout = models.BooleanField(default=False)
    total_price = models.CharField(max_length=300, default="0")
    total_item = models.PositiveIntegerField(default=0)
    success_code = models.CharField(max_length=256, null=True)

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('Cart:cart_detail', kwargs={'id':self.id})



class CartItem(models.Model):
    cart        = models.ForeignKey(Cart, on_delete=models.CASCADE )
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    price       = models.CharField(max_length=300)
    quantity    = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.price
