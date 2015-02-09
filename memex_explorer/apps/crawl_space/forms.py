from django.forms import ModelForm, RadioSelect, Select

from apps.crawl_space.models import Crawl, CrawlModel

from django.core.exceptions import ValidationError

class AddCrawlForm(ModelForm):

    def clean_crawl_model(self):
        crawl_model = self.cleaned_data['crawl_model']
        crawler = self.cleaned_data['crawler']
        if not crawl_model and crawler == 'ache':
            raise ValidationError("Ache Crawls require a crawl model.")

    class Meta:
        model = Crawl
        fields = ['name', 'description', 'crawler', 'crawl_model', 'seeds_list']
        widgets = {'crawler': Select, 'crawl_model': Select}

class AddCrawlModelForm(ModelForm):

    class Meta:
        model = CrawlModel
        fields = ['name', 'model', 'features']

