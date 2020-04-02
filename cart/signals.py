from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from base_shop.models import Cart, CartItem

@receiver(post_save, sender=CartItem)
def add_price_cart(sender, instance, **kwargs):
    cart = Cart.objects.filter(id=instance.cart.id).first()
    price = int((instance.price).replace(",", ""))
    if not cart.total_price:
        cart.total_price = "0"
    else :
        cart.total_price  = int(cart.total_price.replace(",", ""))
    cart.total_price += price
    cart.total_price = '{0:,}'.format(cart.total_price)
    cart.save()


@receiver(post_delete, sender=CartItem)
def remove__price_cart(sender, instance, **kwargs):
    cart = Cart.objects.filter(id=instance.cart.id).first()
    price = int((instance.price).replace(",", ""))
    cart.total_price  = int(cart.total_price.replace(",", ""))
    cart.total_price -= price
    cart.total_price = '{0:,}'.format(cart.total_price)
    cart.save()

@receiver(post_save, sender=CartItem)
def total_item_add(sender, instance, **kwargs):
    cart = Cart.objects.filter(id=instance.cart.id).first()
    cart.total_item = cart.total_item + int(instance.quantity)
    cart.save()
