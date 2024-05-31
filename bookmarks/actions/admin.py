from django.contrib import admin

from .models import Action


# registers models for the actions app
@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    """ActionAdmin registers the :model:`actions.Action` on the administration site. The
    fields are list_display, :filter:`list_filter`, and :filter:`search_fields`.

    Args:
        admin (:model:`actions.Action`): the model to register
    """

    list_display = ["user", "verb", "target", "created"]
    list_filter = ["created"]
    search_fields = ["verb"]
