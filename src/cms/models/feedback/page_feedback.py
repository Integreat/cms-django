from django.db import models

from .feedback import Feedback
from ..pages.page_translation import PageTranslation


class PageFeedback(Feedback):
    """
    Database model representing feedback about pages.

    Fields inherited from the base model :class:`~cms.models.feedback.feedback.Feedback`:

    :param id: The database id of the feedback
    :param emotion: Whether the feedback is positive or negative (choices: :mod:`cms.constants.feedback_emotions`)
    :param comment: A comment describing the feedback
    :param is_technical: Whether or not the feedback is targeted at the developers
    :param read_status: Whether or not the feedback is marked as read
    :param created_date: The date and time when the feedback was created
    :param last_updated: The date and time when the feedback was last updated

    Relationship fields:

    :param page_translation: The page translation the feedback is referring to (related name: ``feedback``)
    :param feedback_ptr: A pointer to the base class
    """

    page_translation = models.ForeignKey(
        PageTranslation, related_name="feedback", on_delete=models.CASCADE
    )

    class Meta:
        default_permissions = ()
