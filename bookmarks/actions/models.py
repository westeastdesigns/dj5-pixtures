from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


# Defines the tables of data for the actions app
class Action(models.Model):
    """Action model stores user activities. The data is indexed in descending order of
    creation date/time. It is also sorted in descending order by creation date/time.
    target_ct points to the model :model:`ContentType`. target_id stores the primary key
    of the related object. target is a GenericForeignKey field to the related object
    based on the combination of target_ct and target_id. target_ct and target_id will be
    mapped to the actual database fields and shown on the admin site.

    Args:
        models (:model:`AUTH_USER_MODEL`): ForeignKey points to the Django :model:`User` model.
        :model:`actions.Action` model fields are user, verb, created, target_ct,
        target_id, and target.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="actions", on_delete=models.CASCADE
    )
    verb = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    target_ct = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        related_name="target_obj",
        on_delete=models.CASCADE,
    )
    target_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey("target_ct", "target_id")

    class Meta:
        indexes = [
            models.Index(fields=["-created"]),
            models.Index(fields=["target_ct", "target_id"]),
        ]
        ordering = ["-created"]
