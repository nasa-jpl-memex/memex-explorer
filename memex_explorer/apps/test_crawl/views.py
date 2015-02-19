import random

from django.views.generic.base import TemplateView
from apps.test_crawl.words import CATS, DOGS

class ContentView(TemplateView):

    template_name = "test_crawl/content.html"
    
    def get_context_data(self, *args, **kwargs):
        context = super(ContentView, self).get_context_data(*args, **kwargs)
        if (int(self.kwargs['content_id']) % 2):
            context['words'] = ' '.join(random.sample(CATS, 1000))
        else:
            context['words'] = ' '.join(random.sample(DOGS, 1000))
        return context
