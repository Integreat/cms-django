from linkcheck.views import report


def linkcheck(request, region_slug):
    return report(request)
