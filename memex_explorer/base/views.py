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
    

class AddProjectView(SuccessMessageMixin, generic.edit.CreateView):
    model = Project
    form_class = AddProjectForm
    template_name = "base/add_project.html"
    success_message = "Project %(name)s was added successfully."

    def get_success_url(self):
        return self.object.get_absolute_url()


class ProjectView(generic.DetailView):
    model = Project
    template_name = "base/project.html"

