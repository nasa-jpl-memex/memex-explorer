from django.forms import ModelForm, RadioSelect, Select
from crispy_forms.helper import FormHelper

from apps.crawl_space.models import Crawl, CrawlModel


class AddCrawlForm(ModelForm):
    class Meta:
        model = Crawl
        fields = ['name', 'description', 'crawler', 'crawl_model', 'seeds_list']
        widgets = {'crawler': Select, 'crawl_model': Select}


class AddCrawlModelForm(ModelForm):
    class Meta:
        model = CrawlModel
        fields = ['name', 'model', 'features']
