from django.utils.translation import ugettext_lazy
from django.views.generic.base import ContextMixin

# pylint: disable=too-few-public-methods
class EventContextMixin(ContextMixin):
    """
    This mixin provides extra context for event views
    """

    #: A dictionary of additional context
    extra_context = {
        "archive_dialog_title": ugettext_lazy(
            "Please confirm that you really want to archive this event"
        ),
        "archive_dialog_text": ugettext_lazy(
            "All translations of this event will also be archived."
        ),
        "restore_dialog_title": ugettext_lazy(
            "Please confirm that you really want to restore this event"
        ),
        "restore_dialog_text": ugettext_lazy(
            "All translations of this event will also be restored."
        ),
        "delete_dialog_title": ugettext_lazy(
            "Please confirm that you really want to delete this event"
        ),
        "delete_dialog_text": ugettext_lazy(
            "All translations of this event will also be deleted."
        ),
    }
