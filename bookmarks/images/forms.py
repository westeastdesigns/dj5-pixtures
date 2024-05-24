from django import forms

from .models import Image


class ImageCreateForm(forms.ModelForm):
    """ImageCreateForm defines a ModelForm form from the Image model, including the
    title, url, and description fields. Users don't enter the url directly in the form.
    A JavaScript tool will let the user pick an image from an external site. The form
    receives the url of the image as a parameter.

    Args:
        forms (ModelForm): includes the title, url, and description fields from Image
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
