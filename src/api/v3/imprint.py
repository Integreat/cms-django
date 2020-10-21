"""
imprint API endpoint
"""
from django.http import JsonResponse

from cms.models import Region


def transform_imprint(imprint_translation):
    """
    Function to create a JSON from a single imprint_translation object.

    :param imprint_translation: single page translation object
    :type imprint_translation: ~cms.models.pages.page_translation.PageTranslation

    :return: return data necessary for API
    :rtype: dict
    """
    return {
        "id": imprint_translation.id,
        "url": imprint_translation.permalink,
        "title": imprint_translation.title,
        "modified_gmt": imprint_translation.last_updated,
        "excerpt": imprint_translation.text,
        "content": imprint_translation.text,
        "parent": None,
        "available_languages": imprint_translation.available_languages,
        "thumbnail": None,
        "hash": None,
    }


# pylint: disable=unused-argument
def imprint(request, region_slug, language_code):
    """
    Get imprint for language and return JSON object to client

    :param request: Django request
    :type request: ~django.http.HttpRequest
    :param region_slug: slug of a region
    :type region_slug: str
    :param language_code: language code
    :type language_code: str

    :return: JSON object according to APIv3 imprint endpoint definition
    :rtype: ~django.http.JsonResponse
    """
    region = Region.get_current_region(request)
    result = []
    imprint_translation = region.imprint.get_public_translation(language_code)
    if imprint_translation:
        result.append(transform_imprint(imprint_translation))
    return JsonResponse(
        result, safe=False
    )  # Turn off Safe-Mode to allow serializing arrays
