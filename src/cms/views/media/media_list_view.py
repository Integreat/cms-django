"""
The module is working as the view component for the dynamic data loading for the media library.
Therefore, it's managing the region permissions and connects the different data structures.
Especially, the root file, the use of the file defined in the Document and the different meta data.
"""
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from ...decorators import region_permission_required, staff_required
from ...models import Document, Region
from ...models.media.directory import Directory


@method_decorator(login_required, name="dispatch")
@method_decorator(region_permission_required, name="dispatch")
class MediaListView(TemplateView):
    """
    Class representing the media management and renders the dynamic data into the HTML template.
    """

    template_name = "media/media_list.html"
    #: The context dict passed to the template (see :class:`~django.views.generic.base.ContextMixin`)
    base_context = {"current_menu_item": "media"}

    def get(self, request, *args, **kwargs):
        """
        Render media list
        """

        return render(
            request,
            self.template_name,
            {
                **self.base_context,
            },
        )


@method_decorator(login_required, name="dispatch")
@method_decorator(staff_required, name="dispatch")
class AdminMediaListView(TemplateView):
    """
    Class representing the media management and renders the dynamic data into the HTML template.
    """

    template_name = "media/media_list_admin.html"
    #: The context dict passed to the template (see :class:`~django.views.generic.base.ContextMixin`)
    base_context = {"current_menu_item": "media"}

    def get(self, request, *args, **kwargs):
        """
        Render media list
        """

        return render(
            request,
            self.template_name,
            {
                **self.base_context,
            },
        )
