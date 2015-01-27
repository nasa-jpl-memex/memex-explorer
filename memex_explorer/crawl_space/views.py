from django.views import generic

from crawl_space.models import Crawl
from crawl_space.forms import AddCrawlForm


class AddCrawlView(generic.edit.CreateView):
    form_class = AddCrawlForm
    template_name = "crawl_space/add_crawl.html"
    success_url = "/"


class CrawlView(generic.DetailView):
    model = Crawl
    template_name = "crawl_space/crawl.html"
