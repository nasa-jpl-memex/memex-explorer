from django.conf.urls import patterns, url

from apps.crawl_space import views

urlpatterns = patterns('',
    url(r'^add_crawl/$', views.AddCrawlView.as_view(), name='add_crawl'),
    url(r'^add_crawl_model/$', views.AddCrawlModelView.as_view(), name='add_crawl_model'),
    url(r'^crawls/$', views.ListCrawlsView.as_view(), name='crawls'),

    url(r'^crawls/(?P<crawl_slug>[\w-]+)/$', views.CrawlView.as_view(), name='crawl'),
)
