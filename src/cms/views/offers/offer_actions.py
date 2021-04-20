"""
This module contains view actions for offer objects.
"""
import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST

from ...decorators import region_permission_required, permission_required
from ...models import Region, Offer, OfferTemplate

logger = logging.getLogger(__name__)


@require_POST
@login_required
@region_permission_required
@permission_required("cms.change_offer")
def activate(request, region_slug, offer_template_slug):
    """
    This view activates an offer for a specific region by creating an :class:`~cms.models.offers.offer.Offer` object

    :param request: The current request
    :type request: ~django.http.HttpResponse

    :param region_slug: The slug of the current region
    :type region_slug: str

    :param offer_template_slug: The slug of the offer template which should be activated for this region
    :type offer_template_slug: str

    :return: A redirection to the media library
    :rtype: ~django.http.HttpResponseRedirect
    """
    region = Region.get_current_region(request)
    template = get_object_or_404(OfferTemplate, slug=offer_template_slug)

    offer = Offer.objects.create(region=region, template=template)
    messages.success(
        request, _("Offer {} was successfully activated").format(offer.name)
    )
    logger.debug("%r activated by %r", offer, request.user.profile)
    return redirect(
        "offers",
        **{
            "region_slug": region_slug,
        }
    )


@require_POST
@login_required
@region_permission_required
@permission_required("cms.change_offer")
def deactivate(request, region_slug, offer_template_slug):
    """
    This view deactivates an offer for a specific region by deleting the respective
    :class:`~cms.models.offers.offer.Offer` object

    :param request: The current request
    :type request: ~django.http.HttpResponse

    :param region_slug: The slug of the current region
    :type region_slug: str

    :param offer_template_slug: The slug of the offer template which should be deactivated for this region
    :type offer_template_slug: str

    :return: A redirection to the media library
    :rtype: ~django.http.HttpResponseRedirect
    """
    region = Region.get_current_region(request)
    template = get_object_or_404(OfferTemplate, slug=offer_template_slug)
    offer = get_object_or_404(region.offers, template=template)

    messages.success(
        request, _("Offer {} was successfully deactivated").format(offer.name)
    )
    logger.debug("%r deactivated by %r", offer, request.user.profile)
    offer.delete()
    return redirect(
        "offers",
        **{
            "region_slug": region_slug,
        }
    )
