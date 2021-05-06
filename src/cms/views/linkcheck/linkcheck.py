from django.db.models import Q
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.base import RedirectView

from linkcheck.models import Link


class LinkListView(ListView):

    template_name = "linkcheck/links_by_filter.html"
    
    def get_queryset(self):
        region_slug = self.kwargs.get("region_slug")
        link_filter = self.kwargs.get("link_filter")
        qset = Link.objects.filter(
            Q(page_translations__page__region__slug=region_slug) |
            Q(event_translations__event__region__slug=region_slug) |
            Q(poi_translations__poi__region__slug=region_slug)
        )
        qset = qset.order_by('-url__last_checked')
        if link_filter == "valid":
            qset = qset.filter(ignore=False, url__status__exact=True)
        elif link_filter == "unchecked":
            qset = qset.filter(ignore=False, url__last_checked__exact=None)
        elif link_filter == "ignored":
            qset = qset.filter(ignore=True)
        else:
            qset = qset.filter(ignore=False, url__status__exact=False)
        return qset

class LinkListRedirectBiew(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        kwargs.update({"link_filter": "invalid"})
        return reverse("linkcheck", kwargs=kwargs)