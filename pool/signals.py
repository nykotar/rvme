from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import PoolTarget


@receiver(pre_delete, sender=PoolTarget)
def delete_image(sender, instance, using, **kwargs):
    instance.feedback_img.delete()
