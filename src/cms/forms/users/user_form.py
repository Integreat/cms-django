import logging

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import (
    validate_password,
    password_validators_help_texts,
)
from django.utils.translation import ugettext_lazy as _

from ..custom_model_form import CustomModelForm
from ...models import Role

logger = logging.getLogger(__name__)


class UserForm(CustomModelForm):
    """
    Form for creating and modifying user objects
    """

    roles = forms.ModelMultipleChoiceField(
        queryset=Role.objects.filter(staff_role=False), required=False
    )
    staff_roles = forms.ModelMultipleChoiceField(
        queryset=Role.objects.filter(staff_role=True), required=False
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        validators=[validate_password],
        help_text=password_validators_help_texts,
        required=False,
    )

    class Meta:
        """
        This class contains additional meta configuration of the form class, see the :class:`django.forms.ModelForm`
        for more information.
        """

        #: The model of this :class:`django.forms.ModelForm`
        model = get_user_model()
        #: The fields of the model which should be handled by this form
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "is_active",
            "is_superuser",
        ]

    def __init__(self, data=None, instance=None):

        # instantiate ModelForm
        super().__init__(data=data, instance=instance)

        # check if user instance already exists
        if self.instance.id:
            # set initial role data
            self.fields["roles"].initial = self.instance.profile.roles
            self.fields["staff_roles"].initial = self.instance.profile.roles
            # don't require password if user already exists
            self.fields["password"].required = False
            # adapt placeholder of password input field
            self.fields["password"].widget.attrs.update(
                {"placeholder": _("Leave empty to keep unchanged")}
            )
        else:
            self.fields["is_active"].initial = False
        # fix password label
        self.fields["password"].label = _("Password")
        self.fields["email"].required = True

    # pylint: disable=signature-differs
    def save(self, *args, **kwargs):
        """
        This method extends the default ``save()``-method of the base :class:`~django.forms.ModelForm` to set attributes
        which are not directly determined by input fields.

        :param args: The supplied arguments
        :type args: list

        :param kwargs: The supplied keyword arguments
        :type kwargs: dict

        :return: The saved user object
        :rtype: ~django.contrib.auth.models.User
        """

        # save ModelForm
        user = super().save(*args, **kwargs)

        # check if password field was changed
        if self.cleaned_data["password"]:
            # change password
            user.set_password(self.cleaned_data["password"])
            user.save()

        if user.is_staff:
            roles = self.cleaned_data["staff_roles"]
        else:
            roles = self.cleaned_data["roles"]

        # assign all selected roles which the user does not have already
        for role in set(roles) - {group.role for group in user.groups.all()}:
            role.group.user_set.add(user)
            if hasattr(user, "profile"):
                logger.info("%r was assigned to %r", role, user.profile)
            else:
                logger.info("%r was assigned to %r", role, user)

        if hasattr(user, "profile"):
            # remove all unselected roles which the user had before
            for role in set(user.profile.roles) - set(roles):
                role.group.user_set.remove(user)
                logger.info("%r was removed from %r", role, user.profile)

        return user

    def clean(self):
        """
        Validate form fields which depend on each other, see :meth:`django.forms.Form.clean`

        :return: The cleaned form data
        :rtype: dict
        """
        cleaned_data = super().clean()
        logger.debug("UserForm cleaned [1/2] with cleaned data %r", cleaned_data)

        # make self.data mutable to allow values to be changed manually
        self.data = self.data.copy()

        if cleaned_data.get("is_staff") and cleaned_data["roles"]:
            logger.warning("Staff member %r can only have staff roles", self.instance)
            self.add_error(
                "roles",
                forms.ValidationError(
                    _("Staff members can only have staff roles"),
                    code="invalid",
                ),
            )
        elif not cleaned_data.get("is_staff") and cleaned_data["staff_roles"]:
            logger.warning("Non-staff member %r cannot have staff roles", self.instance)
            self.add_error(
                "roles",
                forms.ValidationError(
                    _("Only staff members can have staff roles"),
                    code="invalid",
                ),
            )

        logger.debug("UserForm cleaned [2/2] with cleaned data %r", cleaned_data)

        return cleaned_data
