import logging

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.shortcuts import render

from ...models import PageTranslation, Region
from ...decorators import region_permission_required

logger = logging.getLogger(__name__)


@method_decorator(login_required, name="dispatch")
@method_decorator(region_permission_required, name="dispatch")
class TranslationCoverageView(TemplateView):
    """
    View to calculate and show the translation coverage statistics (up to date translations, missing translation, etc)
    """

    #: The template to render (see :class:`~django.views.generic.base.TemplateResponseMixin`)
    template_name = "analytics/translation_coverage.html"
    #: The context dict passed to the template (see :class:`~django.views.generic.base.ContextMixin`)
    base_context = {"current_menu_item": "translation_coverage"}

    def get(self, request, *args, **kwargs):
        """
        Render the translation coverage

        :param request: Object representing the user call
        :type request: ~django.http.HttpRequest

        :param args: The supplied arguments
        :type args: list

        :param kwargs: The supplied keyword arguments
        :type kwargs: dict

        :return: The rendered template response
        :rtype: ~django.template.response.TemplateResponse
        """

        region = Region.get_current_region(request)
        num_pages = region.pages.count()
        languages = []

        for language in region.languages:
            page_translations = PageTranslation.get_translations(region, language)
            languages.append(
                {
                    "translated_name": language.translated_name,
                    "num_page_translations_up_to_date": len(
                        [t for t in page_translations if t.is_up_to_date]
                    ),
                    "num_page_translations_currently_in_translation": len(
                        [t for t in page_translations if t.currently_in_translation]
                    ),
                    "num_page_translations_outdated": len(
                        [t for t in page_translations if t.is_outdated]
                    ),
                    "num_page_translations_missing": num_pages
                    - page_translations.count(),
                }
            )

        return render(
            request, self.template_name, {**self.base_context, "languages": languages}
        )
