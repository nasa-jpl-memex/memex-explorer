from base.forms import CrispyModelForm

from django.forms import ModelForm, RadioSelect, Select
from crispy_forms.layout import Layout, Fieldset, Submit
from crispy_forms.bootstrap import InlineRadios, FormActions

from apps.crawl_space.models import Crawl, CrawlModel

from django.core.exceptions import ValidationError


class AddCrawlForm(CrispyModelForm):

    def clean_crawl_model(self):
        crawl_model = self.cleaned_data['crawl_model']
        try:
            crawler = self.cleaned_data['crawler']
        except KeyError:
            raise ValidationError("Incorrect crawler type.")
        if not crawl_model and crawler == 'ache':
            raise ValidationError("Ache Crawls require a crawl model.")

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

