import cloudinary.uploader
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from .models import Recipe


@receiver(post_delete, sender=Recipe)
def photo_delete(sender, instance, **kwargs):
    if instance.image:
        cloudinary.uploader.destroy(instance.image.public_id)


@receiver(pre_save, sender=Recipe)
def photo_delete_on_change(sender, instance, **kwargs):
    """Deletes old image from Cloudinary when a new one is uploaded"""
    if not instance.pk:
        return False

    try:
        old_file = Recipe.objects.get(pk=instance.pk).image
    except Recipe.DoesNotExist:
        return False

    new_file = instance.image
    if old_file and old_file != new_file:
        cloudinary.uploader.destroy(old_file.public_id)
