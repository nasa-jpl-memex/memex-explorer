from django.conf.urls import patterns, include, url

from base import views


urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^about/$', views.AboutView.as_view(), name='about'),

    # project/
    url(r'^project/add_project/$', views.AddProjectView.as_view(),
        name='add_project'),
    url(r'^project/(?P<slug>[\w-]+)/$', views.ProjectView.as_view(),
        name='project'),

    # # Try other "_space" applications
    url(r'^project/(?P<slug>[\w-]+)/crawl/', include('apps.crawl_space.urls',
        namespace="crawl_space")),
)
