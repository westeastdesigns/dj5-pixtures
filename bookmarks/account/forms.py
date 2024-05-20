from django import forms


class LoginForm(forms.Form):
    """LoginForm authenticates users against the database.

    Args:
        forms (CharField): username
        forms (CharField): password with PasswordInput widget
    """

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
