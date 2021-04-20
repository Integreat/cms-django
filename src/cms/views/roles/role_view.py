import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView

from ...decorators import staff_required, permission_required
from ...forms import RoleForm, GroupForm
from ...models import Role

logger = logging.getLogger(__name__)


@method_decorator(login_required, name="dispatch")
@method_decorator(staff_required, name="dispatch")
@method_decorator(permission_required("cms.view_group"), name="dispatch")
@method_decorator(permission_required("cms.change_group"), name="post")
class RoleView(TemplateView):
    """
    View for the role form
    """

    #: The template to render (see :class:`~django.views.generic.base.TemplateResponseMixin`)
    template_name = "roles/role.html"
    #: The context dict passed to the template (see :class:`~django.views.generic.base.ContextMixin`)
    base_context = {"current_menu_item": "roles"}

    def get(self, request, *args, **kwargs):
        """
        Render :class:`~cms.forms.roles.role_form.RoleForm`

        :param request: The current request
        :type request: ~django.http.HttpResponse

        :param args: The supplied arguments
        :type args: list

        :param kwargs: The supplied keyword arguments
        :type kwargs: dict

        :return: The rendered template response
        :rtype: ~django.template.response.TemplateResponse
        """
        role_instance = Role.objects.filter(id=kwargs.get("role_id")).first()
        group_instance = Group.objects.filter(role=role_instance).first()
        role_form = RoleForm(instance=role_instance)
        group_form = GroupForm(instance=group_instance)
        return render(
            request,
            self.template_name,
            {"role_form": role_form, "group_form": group_form, **self.base_context},
        )

    # pylint: disable=unused-argument
    def post(self, request, *args, **kwargs):
        """
        Submit :class:`~cms.forms.roles.role_form.RoleForm` and save :class:`~django.contrib.auth.models.Group` object

        :param request: The current request
        :type request: ~django.http.HttpResponse

        :param args: The supplied arguments
        :type args: list

        :param kwargs: The supplied keyword arguments
        :type kwargs: dict

        :return: The rendered template response
        :rtype: ~django.template.response.TemplateResponse
        """
        role_instance = Role.objects.filter(id=kwargs.get("role_id")).first()
        group_instance = Group.objects.filter(role=role_instance).first()
        role_form = RoleForm(request.POST, instance=role_instance)
        group_form = GroupForm(request.POST, instance=group_instance)

        if role_form.is_valid() and group_form.is_valid():
            group = group_form.save()
            role_form.instance.group = group
            role = role_form.save()

            if role_instance:
                messages.success(
                    request, _('Role "{}" was successfully saved').format(role)
                )
            else:
                messages.success(
                    request, _('Role "{}" was successfully created').format(role)
                )
        else:
            # TODO: improve messages
            messages.error(request, _("Errors have occurred"))

        return render(
            request,
            self.template_name,
            {"role_form": role_form, "group_form": group_form, **self.base_context},
        )
