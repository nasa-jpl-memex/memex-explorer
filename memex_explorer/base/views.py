"""Base views."""

from django.shortcuts import render
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin

from base.models import Project
from base.forms import AddProjectForm


def project_context_processor(request):
    return {
        'projects': Project.objects.all()
    }


class IndexView(generic.ListView):
    model = Project
    template_name = "base/index.html"


class AboutView(generic.TemplateView):
    template_name = "base/about.html"
    

class AddProjectView(generic.edit.CreateView, SuccessMessageMixin):
    model = Project
    form_class = AddProjectForm
    template_name = "base/add_project.html"
    success_message = "%(name)s was saved successfully."

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data,
                                           name=self.object.name)


class ProjectView(generic.DetailView):
    model = Project
    template_name = "base/project.html"
