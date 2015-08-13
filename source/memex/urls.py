from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest import router


urlpatterns = patterns('',
    url(r'', include('base.urls', namespace="base")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
