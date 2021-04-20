import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView

from backend.settings import PER_PAGE

from ...decorators import region_permission_required, permission_required
from ...models import Region, Language
from .poi_context_mixin import POIContextMixin

logger = logging.getLogger(__name__)


@method_decorator(login_required, name="dispatch")
@method_decorator(region_permission_required, name="dispatch")
@method_decorator(permission_required("cms.view_poi"), name="dispatch")
class POIListView(TemplateView, POIContextMixin):
    """
    View for listing POIs (points of interests)
    """

    #: Template for list of non-archived POIs
    template = "pois/poi_list.html"
    #: Template for list of archived POIs
    template_archived = "pois/poi_list_archived.html"
    #: Whether or not to show archived POIs
    archived = False

    @property
    def template_name(self):
        """
        Select correct HTML template, depending on :attr:`~cms.views.pois.poi_list_view.POIListView.archived` flag
        (see :class:`~django.views.generic.base.TemplateResponseMixin`)

        :return: Path to HTML template
        :rtype: str
        """
        return self.template_archived if self.archived else self.template

    def get(self, request, *args, **kwargs):
        """
        Render POI list

        :param request: The current request
        :type request: ~django.http.HttpResponse

        :param args: The supplied arguments
        :type args: list

        :param kwargs: The supplied keyword arguments
        :type kwargs: dict

        :return: The rendered template response
        :rtype: ~django.template.response.TemplateResponse
        """

        # current region
        region_slug = kwargs.get("region_slug")
        region = Region.get_current_region(request)

        # current language
        language_slug = kwargs.get("language_slug")
        if language_slug:
            language = Language.objects.get(slug=language_slug)
        elif region.default_language:
            return redirect(
                "pois",
                **{
                    "region_slug": region_slug,
                    "language_slug": region.default_language.slug,
                }
            )
        else:
            messages.error(
                request,
                _(
                    "Please create at least one language node before creating locations."
                ),
            )
            return redirect(
                "language_tree",
                **{
                    "region_slug": region_slug,
                }
            )

        if language != region.default_language:
            messages.warning(
                request,
                _(
                    "You can only create locations in the default language (%(language)s)."
                )
                % {"language": region.default_language.translated_name},
            )
        pois = region.pois.filter(archived=self.archived)
        # for consistent pagination querysets should be ordered
        paginator = Paginator(pois.order_by("region__slug"), PER_PAGE)
        chunk = request.GET.get("chunk")
        poi_chunk = paginator.get_page(chunk)
        context = self.get_context_data(**kwargs)
        return render(
            request,
            self.template_name,
            {
                "current_menu_item": "pois",
                "pois": poi_chunk,
                "archived_count": region.pois.filter(archived=True).count(),
                "language": language,
                "languages": region.languages,
                **context,
            },
        )
