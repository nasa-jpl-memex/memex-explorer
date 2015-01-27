from django.conf.urls import patterns, url

from crawl_space import views

urlpatterns = patterns('',
    url(r'^add_crawl/$', views.AddCrawlView.as_view(), name='add_crawl'),
)
