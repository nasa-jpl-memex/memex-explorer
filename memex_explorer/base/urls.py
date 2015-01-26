from django.conf.urls import patterns, url

from base import views


urlpatterns = patterns('',
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^add_project/', views.AddProject.as_view(), name='add_project'),
    url(r'^(?P<slug>[\w-]+)/$', views.Project.as_view(), name='project'),
)

