from base.forms import CrispyModelForm

from django.forms import ModelForm, RadioSelect, Select
from crispy_forms.layout import Layout, Fieldset, Submit
from crispy_forms.bootstrap import InlineRadios, FormActions

from apps.crawl_space.models import Crawl, CrawlModel


class AddCrawlForm(CrispyModelForm):

    class Meta:
        model = Crawl
        fields = ['name', 'description', 'crawler', 'crawl_model', 'seeds_list']
        widgets = {'crawl_model': Select}


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_layout()


    def set_layout(self):

        self.helper.layout = Layout(
            Fieldset(None,
                'name',
                'description',
                InlineRadios(
                    'crawler'),
                'crawl_model',
                'seeds_list',
                FormActions(
                    Submit('submit', "Submit"))
            )
        )


class AddCrawlModelForm(ModelForm):
    class Meta:
        model = CrawlModel
        fields = ['name', 'model', 'features']
