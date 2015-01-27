from django.forms import ModelForm

from crawl_space.models import Crawl


class AddCrawlForm(ModelForm):
    class Meta:
        model = Crawl
        fields = ['name', 'description', 'crawler']
