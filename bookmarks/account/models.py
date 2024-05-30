from django.conf import settings
from django.contrib.auth import get_user_model
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


class Contact(models.Model):
    """Contact model contains a many-to-many relationship between users; those models
    are based on Django's User model. Contact is an intermediate model for that
    relationship, so that it does not alter the User model and stores the time that the
    relationship was created.

    Args:
        models (user): contains variables for user_from, user_to, and created.

    Returns:
        string: a string is returned with the names of the users in the relationship. It
        also is indexed in descending order, by the time the relationship was created.
            user_from: the user who chooses to follow another user, user_to
            user_to: the user who is being followed by user_from
    """

    user_from = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="rel_from_set", on_delete=models.CASCADE
    )
    user_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="rel_to_set", on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["-created"]),
        ]
        ordering = ["-created"]

    def __str__(self):
        return f"{self.user_from} follows {self.user_to}"


# dynamically add the following fields to User
user_model = get_user_model()
user_model.add_to_class(
    "following",
    models.ManyToManyField(
        "self", through=Contact, related_name="followers", symmetrical=False
    ),
)
