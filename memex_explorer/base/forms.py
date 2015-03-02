"""Provides base forms, configured via django-crispy-forms.

The `AddProjectForm` form represents the simplest instance."""

from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

from base.models import Project


class CrispyModelForm(ModelForm):
    """Make Django model forms "crispy", a la django-crispy-forms."""
    
    def __init__(self, *args, **kwargs):
        """Initialize with a FormHelper and default submit action."""

        super(CrispyModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(
            FormActions(Submit('submit', "Submit")))


class AddProjectForm(CrispyModelForm):
    """Add Project crispy model form."""

    def clean_name(self):
        name = self.cleaned_data['name']
        if slugify(unicode(name)) in [x.slug for x in Project.objects.all()]:
            raise ValidationError("Project with this Name already exists.")
        return name

    class Meta:
        model = Project
        fields = ['name', 'description']


class ProjectSettingsForm(AddProjectForm):
    """Change the settings of a project."""

    def __init__(self, *args, **kwargs):
        self.project_instance = kwargs["instance"]
        super(ProjectSettingsForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        new_slug = slugify(unicode(self.cleaned_data["name"]))
        instance_slug = self.project_instance.slug
        slugs = [x.slug for x in Project.objects.exclude(slug=instance_slug)]
        if new_slug in slugs:
            raise ValidationError("Project with this Name already exists.")
        return self.cleaned_data["name"]

