"""
Form for creating a user object
"""
import logging

from django import forms
from django.utils.translation import ugettext_lazy as _

from ...models import UserProfile
from ...utils.translation_utils import ugettext_many_lazy as __
from ..custom_model_form import CustomModelForm

logger = logging.getLogger(__name__)


class UserProfileForm(CustomModelForm):
    """
    Form for creating and modifying user profile objects
    """

    send_activation_link = forms.BooleanField(
        initial=True,
        required=False,
        label=_("Send activation link"),
        help_text=__(
            _(
                "Select this option to create an inactive user account and send an activation link per email to the user."
            ),
            _(
                "This link allows the user to choose a password and activates the account after confirmation."
            ),
        ),
    )

    class Meta:
        """
        This class contains additional meta configuration of the form class, see the :class:`django.forms.ModelForm`
        for more information.
        """

        #: The model of this :class:`django.forms.ModelForm`
        model = UserProfile
        #: The fields of the model which should be handled by this form
        fields = ["regions", "organization", "expert_mode"]

    # pylint: disable=signature-differs
    def save(self, *args, **kwargs):
        """
        This method extends the default ``save()``-method of the base :class:`~django.forms.ModelForm` to set attributes
        which are not directly determined by input fields.

        :param args: The supplied arguments
        :type args: list

        :param kwargs: The supplied keyword arguments
        :type kwargs: dict

        :return: The saved user profile object
        :rtype: ~cms.models.users.user_profile.UserProfile
        """

        # pop kwarg to make sure the super class does not get this param
        user = kwargs.pop("user", None)

        if not self.instance.id:
            # don't commit saving of ModelForm, because required user field is still missing
            kwargs["commit"] = False

        # save ModelForm
        user_profile = super().save(*args, **kwargs)

        if not self.instance.id:
            user_profile.user = user
            user_profile.save()
            # check if called from UserProfileForm or RegionUserProfileForm
            if "regions" in self.cleaned_data:
                # regions can't be saved if commit=False on the ModelForm, so we have to save them explicitly
                user_profile.regions.set(self.cleaned_data["regions"])

        return user_profile
