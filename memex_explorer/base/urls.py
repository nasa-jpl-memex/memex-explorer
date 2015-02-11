from django.conf.urls import patterns, include, url
from base import views


project_slug = r'^projects/(?P<slug>[\w-]+)/'

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),       # Index
    url(r'^about/$', views.AboutView.as_view(), name='about'), # About

    url(r'^add_project/$', views.AddProjectView.as_view(),
        name='add_project'),                                   # Add Project
    url(project_slug + r'$', views.ProjectView.as_view(),
        name='project')                                        # Project
)



# The following lines build a url route to each application listed in
#   `settings.EXPLORER_APPS`, namespaced appropriately.
#   See <https://github.com/ContinuumIO/memex-explorer/issues/316>

from django.conf import settings

inject_urls = [
    url(project_slug, include('apps.%s.urls' % app, namespace=app))
    for app in settings.EXPLORER_APPS
]

urlpatterns += patterns('', *inject_urls)
