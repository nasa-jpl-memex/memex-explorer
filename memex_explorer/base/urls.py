"""Base url routes.

This module also dynamically adds url routes to applications present in
INSTALLED_APPS; see the comments below.

URLs
----

/
about/
add_project/
project/

"""

from django.conf.urls import patterns, include, url
from base import views


project_slug = r'^projects/(?P<slug>[\w-]+)/'

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),

    url(r'^about/$', views.AboutView.as_view(), name='about'),

    url(r'^add_project/$', views.AddProjectView.as_view(),
        name='add_project'),
    
    url(project_slug + r'$', views.ProjectView.as_view(),
        name='project')
)


# The following lines "discover" Django applications in INSTALLED_APPS
#   and include a url route to each application, namespaced appropriately.
#   See <https://github.com/ContinuumIO/memex-explorer/issues/316>

from django.conf import settings
space_apps = [
    x.lstrip("apps.") for x in settings.INSTALLED_APPS
    if "_space" in x
]

inject_urls = [
    url(project_slug, include('apps.%s.urls' % app, namespace=app))
    for app in space_apps
]

urlpatterns += patterns('', *inject_urls)
