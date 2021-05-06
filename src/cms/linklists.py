from linkcheck import Linklist

from .models import PageTranslation, EventTranslation, POITranslation


class PageTranslationLinklist(Linklist):

    model = PageTranslation
    html_fields = ["text"]

class EventTranslationLinklist(Linklist):

    model = EventTranslation
    html_fields = ["description"]

class POITranslationLinklist(Linklist):

    model = POITranslation
    html_fields = ["description"]

linklists = {
    "PageTranslations": PageTranslationLinklist,
    "EventTranslations": EventTranslationLinklist,
    "POITranslations": POITranslationLinklist,
}
