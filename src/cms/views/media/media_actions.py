"""
This module contains view actions for media related objects.
"""
import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_POST

from ...decorators import region_permission_required
from ...models import Document, Region, Directory
from ...utils.media_utils import attach_file, delete_document


@require_POST
@login_required
@region_permission_required
# pylint: disable=unused-argument
def delete_file(request, document_id, region_slug):
    """
    This view deletes a file both from the database and the file system.

    :param request: The current request
    :type request: ~django.http.HttpResponse

    :param document_id: The id of the document which is being deleted
    :type document_id: int

    :param region_slug: The slug of the region to which this document belongs
    :type region_slug: str

    :return: A redirection to the media library
    :rtype: ~django.http.HttpResponseRedirect
    """
    region = Region.get_current_region(request)

    if request.method == "POST":
        document = Document.objects.get(pk=document_id)
        if document.region != region:
            raise PermissionError
        delete_document(document)

    directory_id = 0
    try:
        directory_id = document.directory.id
    except Directory.DoesNotExist:
        pass

    return redirect(
        "media", **{"region_slug": region.slug, "directory_id": directory_id}
    )


@require_POST
@login_required
@region_permission_required
def upload_file_ajax(request, region_slug):
    region = Region.objects.get(slug=region_slug)

    directory_id = request.POST.get("parentDirectory", 0)
    print(directory_id)
    directory = None

    if int(directory_id) != 0:
        directory = Directory.objects.get(id=directory_id)
        if directory.region != region:
            raise PermissionError

    if "upload" in request.FILES:
        document = Document()
        document.region = region
        document.parent_directory = directory
        document.name = request.FILES["upload"].name
        attach_file(document, request.FILES["upload"])
        document.save()
        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": _("No file was uploaded")})


@login_required
@region_permission_required
def get_directory_content_ajax(request, region_slug):
    region = Region.objects.get(slug=region_slug)
    directory_id = request.GET.get("directory")

    directory = None
    if directory_id is not None and int(directory_id) != 0:
        directory = Directory.objects.get(id=directory_id)
        if directory.region != region:
            raise PermissionError

    documents = Document.objects.filter(
        Q(region=region) | Q(region__isnull=True), Q(parent_directory=directory)
    )
    directories = Directory.objects.filter(
        Q(region=region) | Q(region__isnull=True), parent=directory
    )

    result = list(map(lambda directory: directory.serialize(), directories)) + list(
        map(lambda document: document.serialize(), documents)
    )

    return JsonResponse({"success": True, "data": result}, status=200)


@login_required
@region_permission_required
@require_POST
def edit_media_element_ajax(request, region_slug):

    # Check for correct Request. As we are updating a database object, only POST is allowed.
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request."}, status=405)

    json_data = json.loads(request.body.decode("utf-8"))
    media_element_id = json_data["id"]
    media_element = get_object_or_404(Document, id=media_element_id)

    media_element.name = json_data["name"]
    media_element.alt_text = json_data["alt_text"]
    media_element.save()

    return JsonResponse({"success": True}, status=200)


@login_required
@region_permission_required
@require_POST
def create_directory_ajax(request, region_slug):
    region = Region.objects.get(slug=region_slug)
    # Check for correct Request. As we are updating a database object, only POST is allowed.
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request."}, status=405)

    json_data = json.loads(request.body.decode("utf-8"))
    if json_data["parentDirectory"] != 0:
        parent_directory = get_object_or_404(Directory, id=json_data["parentDirectory"])

        if parent_directory.region != region:
            raise PermissionError
    else:
        json_data["parentDirectory"] = None

    if Directory.objects.filter(
        parent=json_data["parentDirectory"], name=json_data["directoryName"]
    ).exists():
        return JsonResponse({"error": _("Directory already exists")}, status=400)

    new_directory = Directory()
    new_directory.name = json_data["directoryName"]
    new_directory.parent = parent_directory
    new_directory.region = region
    new_directory.save()

    return JsonResponse({"success": True})
