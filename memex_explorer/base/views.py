from django.shortcuts import render, get_object_or_404
from django.views import generic

from base.models import Project
from base.forms import AddProjectForm


class Index(generic.ListView):
    model = Project
    template_name = "base/index.html"
    context_object_name = "projects"


class AddProject(generic.edit.CreateView):
    model = Project
    form_class = AddProjectForm
    template_name = "base/add_project.html"
    success_url = "/base"

