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
from ...models import Language, Region

logger = logging.getLogger(__name__)


@method_decorator(login_required, name="dispatch")
@method_decorator(region_permission_required, name="dispatch")
@method_decorator(permission_required("cms.view_push_notification"), name="dispatch")
class PushNotificationListView(TemplateView):
    """
    Class that handles HTTP GET requests for listing push notifications
    """

    #: The template to render (see :class:`~django.views.generic.base.TemplateResponseMixin`)
    template_name = "push_notifications/push_notification_list.html"
    #: The context dict passed to the template (see :class:`~django.views.generic.base.ContextMixin`)
    base_context = {"current_menu_item": "push_notifications"}

    def get(self, request, *args, **kwargs):
        """
        Create a list that shows existing push notifications and translations

        :param request: Object representing the user call
        :type request: ~django.http.HttpRequest

        :param args: The supplied arguments
        :type args: list

        :param kwargs: The supplied keyword arguments
        :type kwargs: dict

        :return: The rendered template response
        :rtype: ~django.template.response.TemplateResponse
        """

        # current region
        region = Region.get_current_region(request)

        # current language
        language_slug = kwargs.get("language_slug")
        if language_slug:
            language = Language.objects.get(slug=language_slug)
        elif region.default_language:
            return redirect(
                "push_notifications",
                **{
                    "region_slug": region.slug,
                    "language_slug": region.default_language.slug,
                }
            )
        else:
            messages.error(
                request,
                _(
                    "Please create at least one language node before creating push notifications."
                ),
            )
            return redirect(
                "language_tree",
                **{
                    "region_slug": region.slug,
                }
            )
        push_notifications = region.push_notifications.all()
        # for consistent pagination querysets should be ordered
        paginator = Paginator(push_notifications.order_by("created_date"), PER_PAGE)
        chunk = request.GET.get("chunk")
        push_notifications_chunk = paginator.get_page(chunk)
        return render(
            request,
            self.template_name,
            {
                **self.base_context,
                "push_notifications": push_notifications_chunk,
                "language": language,
                "languages": region.languages,
            },
        )
