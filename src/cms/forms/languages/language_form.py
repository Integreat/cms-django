from ..custom_model_form import CustomModelForm
from ...models import Language


class LanguageForm(CustomModelForm):
    """
    Form for creating and modifying language objects
    """

    class Meta:
        """
        This class contains additional meta configuration of the form class, see the :class:`django.forms.ModelForm`
        for more information.
        """

        #: The model of this :class:`django.forms.ModelForm`
        model = Language
        #: The fields of the model which should be handled by this form
        fields = [
            "slug",
            "bcp47_tag",
            "english_name",
            "native_name",
            "text_direction",
            "table_of_contents",
        ]
