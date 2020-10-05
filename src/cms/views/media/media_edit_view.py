from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from ...decorators import region_permission_required
from ...forms.media import DocumentForm
from ...models import Document, Region
from ...utils.file_utils import save_file


@method_decorator(login_required, name="dispatch")
@method_decorator(region_permission_required, name="dispatch")
class MediaEditView(TemplateView):
    template_name = "media/media_form.html"
    base_context = {"current_menu_item": "media_upload"}

    def get(self, request, *args, **kwargs):
        region = Region.get_current_region(request)
        document_id = kwargs.get("document_id")
        form = DocumentForm()
        if document_id != "0":
            document = Document.objects.get(id=document_id)
            form = DocumentForm(instance=document)

        return render(
            request,
            self.template_name,
            {
                **self.base_context,
                "form": form,
                "region_slug": region.slug,
            },
        )

    # pylint: disable=unused-argument
    def post(self, request, *args, **kwargs):
        # current region
        region = Region.get_current_region(request)

        result = save_file(request)

        if result.get("status") == 1:
            return redirect("media", **{"region_slug": region.slug})
        return render(request, self.template_name, {"form": result.get("form")})
