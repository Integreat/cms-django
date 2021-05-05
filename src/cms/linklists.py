from linkcheck import Linklist

from .models import PageTranslation


class PageTranslationLinklist(Linklist):

    model = PageTranslation
    html_fields = ["text"]


linklists = {"PageTranslations": PageTranslationLinklist}
