from django.forms import ModelForm

from base.models import Project


class AddProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'icon']

