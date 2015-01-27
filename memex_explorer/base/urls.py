from django.conf.urls import patterns, url

from base import views


urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^project/add_project/$', views.AddProjectView.as_view(), name='add_project'),
    url(r'^project/(?P<slug>[\w-]+)/$', views.ProjectView.as_view(), name='project'),
)

