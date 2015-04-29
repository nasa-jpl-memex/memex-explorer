"""Base views."""
import json
import shutil
import os

from django.shortcuts import render
from django.views import generic
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.http import HttpResponse

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from base.models import Project, Index
from base.forms import AddProjectForm, ProjectSettingsForm, AddIndexForm

from apps.crawl_space.models import Crawl
from apps.crawl_space.settings import CRAWL_PATH
from apps.crawl_space.views import ProjectObjectMixin

from task_manager.tika_tasks import create_index


def project_context_processor(request):
    return {
        'projects': Project.objects.all(),
    }


class IndexView(ListView):
    model = Project
    template_name = "base/index.html"


class AboutView(TemplateView):
    template_name = "base/about.html"


class AddProjectView(SuccessMessageMixin, CreateView):
    model = Project
    form_class = AddProjectForm
    template_name = "base/add_project.html"
    success_message = "Project %(name)s was added successfully."

    def get_success_url(self):
        return self.object.get_absolute_url()


class ProjectView(DetailView):
    model = Project
    slug_url_kwarg = 'project_slug'
    template_name = "base/project.html"

    def get_object(self):
        return Project.objects.get(slug=self.kwargs['project_slug'])


class ProjectSettingsView(SuccessMessageMixin, UpdateView):
    model = Project
    slug_url_kwarg = 'project_slug'
    form_class = ProjectSettingsForm
    success_message = "Project %(name)s was edited successfully."
    template_name_suffix = '_update_form'


class DeleteProjectView(SuccessMessageMixin, DeleteView):
    model = Project
    success_message = "Project %(name)s was deleted successfully."
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        """Remove crawls and folders for crawls."""
        # for crawl in self.get_crawls():
        #     shutil.rmtree(os.path.join(CRAWL_PATH, str(crawl.pk)))
        #     crawl.delete()
        return super(DeleteProjectView, self).delete(request, *args, **kwargs)

    def get_object(self):
        return Project.objects.get(slug=self.kwargs['project_slug'])

    def get_crawls(self):
        return Crawl.objects.filter(project=self.get_object())


class AddIndexView(SuccessMessageMixin, ProjectObjectMixin, CreateView):
    model = Index
    form_class = AddIndexForm
    template_name = "base/add_index.html"
    success_message = "Index %(name)s was added successfully."

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        form.instance.project = self.get_project()
        return super(AddIndexView, self).form_valid(form)

