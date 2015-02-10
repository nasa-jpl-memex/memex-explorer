from django.forms import ModelForm
from crispy_forms.helper import FormHelper

from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

from base.models import Project


class CrispyModelForm(ModelForm):
    """Make Django model forms "crispy", a la django-crispy-forms."""
    
    def __init__(self, *args, **kwargs):
        """Initialize with a FormHelper and default submit action."""

        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(
            FormActions(Submit('submit', "Submit")))


class AddProjectForm(CrispyModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']
