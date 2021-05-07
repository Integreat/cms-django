from itertools import cycle

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.shortcuts import render
from django.utils.translation import ugettext as _

from ...models import PageTranslation, Region
from ...decorators import region_permission_required

from ...constants import colors


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
        # total_number_pages = region.pages.count()

        chart_data = []
        summary_data = []
        total_words = 0
        labels = [
            _("Translations up-to-date"),
            _("Currently in translation"),
            _("Translations outdated"),
            _("Translations missing"),
        ]
        color_cycle = cycle(colors.CHOICES)

        for language in region.languages:
            page_translations = PageTranslation.get_translations(region, language)
            page_translations_up_to_date = 0
            page_translations_in_translation = 0
            page_translations_outdated = 0
            word_count_outdated = 0

            for page_translation in page_translations:
                if page_translation.is_up_to_date:
                    page_translations_up_to_date += 1
                elif page_translation.currently_in_translation:
                    page_translations_in_translation += 1
                elif page_translation.is_outdated:
                    page_translations_outdated += 1
                    word_count_outdated += len(page_translation.text.split())

            chart_data.append(
                {
                    "labels": [region.languages],
                    "datasets": [
                        {
                            "label": labels[1],
                            "borderColor": next(color_cycle),
                            "data": "test",
                        }
                    ],
                }
            )
            summary_data.append(
                {
                    "translated_name": language.translated_name,
                    "word_count": word_count_outdated,
                }
            )
            total_words += word_count_outdated

        return render(
            request,
            self.template_name,
            {
                **self.base_context,
                "coverage_data": chart_data,
                "summary_data": summary_data,
                "total_words": total_words,
            },
        )
