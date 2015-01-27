from django.views import generic

from base.views import WithProjects

from crawl_space.models import Crawl
from crawl_space.forms import AddCrawlForm


class AddCrawlView(generic.edit.CreateView):
    model = Crawl
    form_class = AddCrawlForm
    template_name = "crawl_space/add_crawl.html"
    success_url = "/"


class CrawlView(generic.DetailView):
    model = Crawl
    template_name = "crawl_space/crawl.html"


