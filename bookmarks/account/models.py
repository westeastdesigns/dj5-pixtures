from django.conf import settings
from django.db import models


# Defines the tables of data for the account application
class Profile(models.Model):
    """Profile model contains a 1-to-1 relationship with the Django user model, and any
    additional fields. The Profile model is used to store data for the user's profile.

    Args:
        models (user): contains variables for user, date_of_birth, and photo

    Returns:
        OneToOneField: user model
        DateField: user's date_of_birth
        ImageField: photo field
    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
