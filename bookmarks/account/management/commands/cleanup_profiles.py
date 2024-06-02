# account/management/commands/cleanup_profiles.py

from account.models import Profile
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Ensure all users have a profile and remove duplicates"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        for user in User.objects.all():
            profiles = Profile.objects.filter(user=user)
            if profiles.count() > 1:
                # If there are duplicates, delete the extras
                profiles[1:].delete()
            Profile.objects.get_or_create(user=user)
        self.stdout.write(self.style.SUCCESS("Successfully cleaned up profiles"))
