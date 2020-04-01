from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Manufacturer, Product, MultipleImages

@receiver(post_delete, sender=Product)
@receiver(post_delete, sender=MultipleImages)
@receiver(post_delete, sender=Manufacturer)
def photo_delete_handler(sender, **kwargs):
    photo = kwargs['instance']
    if photo :
        storage, path = photo.image.storage, photo.image.path
        storage.delete(path)
