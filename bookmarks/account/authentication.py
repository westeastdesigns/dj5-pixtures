from django.contrib.auth.models import User

from .models import Profile


# authentication backend
class EmailAuthBackend:
    """Authenticate using an e-mail address."""

    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


# profile creation is now being handled by the signal
# def create_profile(backend, user, *args, **kwargs):
#     """create_profile creates user profile for social authentication

#     Args:
#         backend (AUTHENTICATION_BACKEND): social auth backend used for user authentication
#         user (object): User instance of the new or existing authenticated user
#     """
#     Profile.objects.get_or_create(user=user)


def create_profile(backend, user, response, *args, **kwargs):
    """create_profile creates a Profile object for the user, for social authentication

    Args:
        backend (AUTHENTICATION_BACKEND): social auth backend used for user authentication
        user (object): User instance of the new or existing authenticated user
    """
    if Profile.objects.filter(user=user).exists():
        return
    Profile.objects.create(user=user)
