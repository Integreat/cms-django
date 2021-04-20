import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView

from ...decorators import staff_required, permission_required
from ...forms import RegionForm
from ...models import Region

logger = logging.getLogger(__name__)


@method_decorator(login_required, name="dispatch")
@method_decorator(staff_required, name="dispatch")
@method_decorator(permission_required("cms.view_region"), name="dispatch")
@method_decorator(permission_required("cms.change_region"), name="post")
class RegionView(TemplateView):
    """
    View for the region form
    """

    #: The template to render (see :class:`~django.views.generic.base.TemplateResponseMixin`)
    template_name = "regions/region_form.html"
    #: The context dict passed to the template (see :class:`~django.views.generic.base.ContextMixin`)
    base_context = {"current_menu_item": "regions"}

    def get(self, request, *args, **kwargs):
        """
        Render :class:`~cms.forms.regions.region_form.RegionForm`

        :param request: The current request
        :type request: ~django.http.HttpResponse

        :param args: The supplied arguments
        :type args: list

        :param kwargs: The supplied keyword arguments
        :type kwargs: dict

        :return: The rendered template response
        :rtype: ~django.template.response.TemplateResponse
        """

        region_instance = Region.objects.filter(slug=kwargs.get("region_slug")).first()

        form = RegionForm(instance=region_instance)

        return render(request, self.template_name, {"form": form, **self.base_context})

    # pylint: disable=unused-argument
    def post(self, request, *args, **kwargs):
        """
        Render :class:`~cms.forms.regions.region_form.RegionForm` and save :class:`~cms.models.regions.region.Region`
        object

        :param request: The current request
        :type request: ~django.http.HttpResponse

        :param args: The supplied arguments
        :type args: list

        :param kwargs: The supplied keyword arguments
        :type kwargs: dict

        :return: The rendered template response
        :rtype: ~django.template.response.TemplateResponse
        """

        region_instance = Region.objects.filter(slug=kwargs.get("region_slug")).first()

        form = RegionForm(request.POST, request.FILES, instance=region_instance)

        # TODO: error handling
        if not form.is_valid():
            messages.error(request, _("Errors have occurred."))
            return render(
                request, self.template_name, {"form": form, **self.base_context}
            )

        if not form.has_changed():
            messages.info(request, _("No changes detected."))
            return render(
                request, self.template_name, {"form": form, **self.base_context}
            )

        region = form.save()

        if region_instance:
            messages.success(request, _("Region was saved successfully"))
        else:
            messages.success(request, _("Region was created successfully"))

        return redirect(
            "edit_region",
            **{
                "region_slug": region.slug,
            }
        )
