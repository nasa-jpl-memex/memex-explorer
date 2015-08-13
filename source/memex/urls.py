from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework import routers

from rest import ProjectViewSet


router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)


urlpatterns = patterns('',
    url(r'', include('base.urls', namespace="base")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
