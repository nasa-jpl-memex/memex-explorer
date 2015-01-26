from django.shortcuts import render
from django.views import generic

from base.models import Project
from base.forms import AddProjectForm


def project_context_processor(request):
    return {
        'projects': Project.objects.all()
    }


class IndexView(generic.ListView):
    model = Project
    template_name = "base/index.html"
    context_object_name = "projects"


class AddProjectView(generic.edit.CreateView):
    model = Project
    form_class = AddProjectForm
    template_name = "base/add_project.html"
    success_url = "/"


class ProjectView(generic.DetailView):
    model = Project
    template_name = "base/project.html"

