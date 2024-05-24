import requests
from django import forms
from django.core.files.base import ContentFile
from django.utils.text import slugify

from .models import Image


class ImageCreateForm(forms.ModelForm):
    """ImageCreateForm defines a ModelForm form from the :model:'images.Image', including
    the title, url, and description fields. Users don't enter the url directly in the
    form. A JavaScript tool will let the user pick an image from an external site. The
    form receives the url of the image as a parameter.

    Args:
        forms (ModelForm): includes title, url, and description fields from :model:'images.Image'
    """

    class Meta:
        model = Image
        fields = ["title", "url", "description"]
        widgets = {
            "url": forms.HiddenInput,
        }

    def clean_url(self):
        """clean_url verifies the provided image URL is valid by retrieving the value of
        the url field in the cleaned_data dictionary of the form instance. It then splits
        the url to check if the file extension is valid.

        Raises:
            forms.ValidationError: If the extension isn't in the list of valid_extensions

        Returns:
            URLField: url of image
        """
        url = self.cleaned_data["url"]
        valid_extensions = ["jpg", "jpeg", "png"]
        extension = url.rsplit(".", 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError(
                "The given URL does not match valid image extensions."
            )
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        """save overrides the form's save() method to retrieve the image file by the
        given url and save it to the file system. It keeps the parameters required by
        ModelForm.

        Args:
            force_insert (bool, optional): forces an INSERT. Defaults to False.
            force_update (bool, optional): forces an UPDATE. Defaults to False.
            commit (bool, optional): saves the form to the db if True. Defaults to True.
            Allows specification of whether the object has to be persisted to the db.

        Returns:
            :model:'images.Image' the updated Image model is saved
        """
        image = super().save(commit=False)
        image_url = self.cleaned_data["url"]
        name = slugify(image.title)
        extension = image_url.rsplit(".", 1)[1].lower()
        image_name = f"{name}.{extension}"
        # download image from the given url
        response = requests.get(image_url)
        image.image.save(image_name, ContentFile(response.content), save=False)
        if commit:
            image.save()
        return image
