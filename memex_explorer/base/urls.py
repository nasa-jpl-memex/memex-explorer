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



# The following lines "discover" Django applications in 
#   based on the presence of "_space" in apps.__dict__.keys()—
#   and builds a url route to each application, namespaced appropriately.
#   See <https://github.com/ContinuumIO/memex-explorer/issues/316>

from django.conf import settings
space_apps = [x for x in settings.INSTALLED_APPS if "_space" in x]


inject_urls = [
    url(project_slug, include('apps.%s.urls' % app, namespace=app))
    for app in space_apps
]


urlpatterns += patterns('', *inject_urls)
