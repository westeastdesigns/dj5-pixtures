from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Image


@receiver(m2m_changed, sender=Image.users_like.through)
def users_like_changed(sender, instance, **kwargs):
    """users_like_changed is registered as a receiver function, and is attached to the
    m2m_changed signal. This function is only called if the signal has been launched by
    the sender.

    Args:
        sender (ManyToManyField): related to the users who like an image
        instance (PositiveIntegerField): the number of people who like an image
    """
    instance.total_likes = instance.users_like.count()
    instance.save()
