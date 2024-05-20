from django import forms
from django.contrib.auth import get_user_model

from .models import Profile


class LoginForm(forms.Form):
    """LoginForm authenticates users against the database.

    Args:
        forms (CharField): username
        forms (CharField): password with PasswordInput widget
    """

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    """UserRegistrationForm lets the user enter a username, real name, and password. It
    uses the get_user_model to retrieve the user model dynamically.

    Args:
        forms (CharField): password
        forms (CharField): first_name
    """

    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ["username", "first_name", "email"]

    def clean_password2(self):
        """clean_password2 compares the second password against the first one.

        Raises:
            forms.ValidationError: if the passwords do not match

        Returns:
            CharField: password2
        """
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Passwords don't match.")
        return cd["password2"]


class UserEditForm(forms.ModelForm):
    """UserEditForm lets users edit their first name, last name, and email. All are
    attributes of the built-in Django user model.

    Args:
        forms (user): references the built-in Django model
            (CharField): first_name
            (Charfield): last_name
            (EmailField): email
    """

    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "email"]


class ProfileEditForm(forms.ModelForm):
    """ProfileEditForm lets users edit their profile data stored in the custom Profile
    model. This includes their date of birth and profile photo.

    Args:
        forms (Profile): custom Profile model
            (DateField): date_of_birth
            (ImageField): photo
    """

    class Meta:
        model = Profile
        fields = ["date_of_birth", "photo"]
