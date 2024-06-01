from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# defines tables in the database for the images app data
class Image(models.Model):
    """Image is used to store images in the platform. The images are indexed in
    descending order.

    Args:
        models (ForeignKey) user: many-to-1 relationship between image and user
        (CharField) title: title of the image
        (SlugField) slug: short SEO friendly url label
        (URLField) url: the original url of the image
        (ImageField) image: the image file
        (TextField) description: optional description of image
        (DatetimeField) created: when the object was created in the database
        (ManyToManyField) users_like: stores the users who like an image
        (PositiveIntegerField) total_likes: counts the number of people who like an image

    Returns:
        string: title
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="images_created",
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField(max_length=2000)
    image = models.ImageField(upload_to="images/%Y/%m/%d/")
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    users_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="images_liked",
        blank=True,
    )
    total_likes = models.PositiveIntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=["-created"]),
            models.Index(fields=["-total_likes"]),
        ]
        ordering = ["-created"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """save automatically generates a slug from the title of the image if the slug
        field doesn't have a value when the Image object is saved.
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("images:detail", args=[self.id, self.slug])
