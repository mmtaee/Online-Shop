from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from cart.models import Cart, CartItem

@receiver(post_save, sender=CartItem)
def add_price_cart(sender, instance, created, **kwargs):
    if created:
        price = int((instance.price).replace(",", ""))
        total_price  = int(instance.cart.total_price.replace(",", ""))
        total_price += price
        instance.cart.total_price = '{0:,}'.format(total_price)

        total_item = instance.cart.total_item
        instance.cart.total_item = total_item + int(instance.quantity)
        instance.cart.save()


@receiver(post_delete, sender=CartItem)
def remove__price_cart(sender, instance, **kwargs):
    price = int((instance.price).replace(",", ""))
    total_price  = int(instance.cart.total_price.replace(",", ""))
    total_price -= price
    instance.cart.total_price = '{0:,}'.format(total_price)

    total_item = instance.cart.total_item
    instance.cart.total_item = total_item - int(instance.quantity)
    instance.cart.save()
